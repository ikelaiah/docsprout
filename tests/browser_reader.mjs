// End-to-end reader checks. Run with `npm run test:browser` after installing
// Playwright's Chromium, Firefox and WebKit browsers (see CONTRIBUTING.md).
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {createReadStream} from 'node:fs';
import {mkdir, realpath, stat, writeFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium, firefox, webkit} from 'playwright';

const repository = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const siteDirectory = path.join(repository, 'build', 'reader-site');
const artifactsDirectory = path.join(repository, 'build', 'reader-artifacts');
const mountPath = '/preview/';
const browsers = {chromium, firefox, webkit};
const requestedBrowser = process.env.DOCSPROUT_BROWSER
  || process.argv.find(argument => argument.startsWith('--browser='))?.split('=')[1];
const results = [];
let failure;
const mimeTypes = new Map([
  ['.css', 'text/css; charset=utf-8'], ['.html', 'text/html; charset=utf-8'],
  ['.ico', 'image/x-icon'], ['.js', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'], ['.jpg', 'image/jpeg'],
  ['.jpeg', 'image/jpeg'], ['.png', 'image/png'],
  ['.webp', 'image/webp'], ['.woff', 'font/woff'], ['.woff2', 'font/woff2'],
  ['.svg', 'image/svg+xml'],
]);

async function buildSite() {
  const pythonPath = path.join(repository, 'src');
  const environment = {...process.env};
  environment.PYTHONPATH = environment.PYTHONPATH
    ? `${pythonPath}${path.delimiter}${environment.PYTHONPATH}`
    : pythonPath;
  const result = spawnSync(process.env.PYTHON || 'python', [
    '-m', 'docsprout', 'build', '--output', siteDirectory, '--release', 'browser-test',
  ], {cwd: repository, env: environment, encoding: 'utf8', timeout: 120_000});
  const output = [result.stdout, result.stderr].filter(Boolean).join('\n');
  await writeFile(path.join(artifactsDirectory, 'build.log'), `${output}\n`, 'utf8');
  if (result.error) throw new Error(`Site build failed: ${result.error.message}\n${output}`);
  if (result.status !== 0) throw new Error(`Site build exited with ${result.status}:\n${output}`);
  if (result.stdout) process.stdout.write(result.stdout);
}

async function serveSite() {
  const trustedRoot = await realpath(siteDirectory);
  const server = createServer(async (request, response) => {
    try {
      if (!['GET', 'HEAD'].includes(request.method)) {
        response.writeHead(405, {Allow: 'GET, HEAD'}).end();
        return;
      }
      const requestUrl = new URL(request.url, 'http://localhost');
      if (requestUrl.pathname === mountPath.slice(0, -1)) {
        response.writeHead(308, {Location: mountPath}).end();
        return;
      }
      if (!requestUrl.pathname.startsWith(mountPath)) {
        response.writeHead(404).end();
        return;
      }
      const relativePath = decodeURIComponent(requestUrl.pathname.slice(mountPath.length));
      const candidate = path.resolve(trustedRoot, relativePath || 'index.html');
      const resolvedPath = await realpath(candidate);
      const relativeToRoot = path.relative(trustedRoot, resolvedPath);
      if (relativeToRoot === '..' || relativeToRoot.startsWith(`..${path.sep}`) || path.isAbsolute(relativeToRoot)) {
        response.writeHead(404).end();
        return;
      }
      const info = await stat(resolvedPath);
      if (!info.isFile()) {
        response.writeHead(404).end();
        return;
      }
      response.writeHead(200, {
        'Content-Length': info.size,
        'Content-Type': mimeTypes.get(path.extname(resolvedPath).toLowerCase()) || 'application/octet-stream',
        'X-Content-Type-Options': 'nosniff',
      });
      if (request.method === 'HEAD') response.end();
      else createReadStream(resolvedPath).pipe(response);
    } catch {
      response.writeHead(404).end();
    }
  });
  try {
    await withTimeout(new Promise((resolve, reject) => {
      server.once('error', reject);
      server.listen(0, '127.0.0.1', resolve);
    }), 'Local server startup readiness');
  } catch (error) {
    await new Promise(resolve => server.close(() => resolve()));
    throw error;
  }
  const address = server.address();
  return {server, baseUrl: `http://127.0.0.1:${address.port}${mountPath}`};
}

function withTimeout(promise, description, timeoutMs = 10_000) {
  let timeout;
  const timedOut = new Promise((_, reject) => {
    timeout = setTimeout(() => reject(new Error(`${description} timed out after ${timeoutMs}ms`)), timeoutMs);
  });
  return Promise.race([promise, timedOut]).finally(() => clearTimeout(timeout));
}

async function openPage(browser, baseUrl, recordErrors) {
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const page = await context.newPage();
  page.setDefaultTimeout(10_000);
  page.setDefaultNavigationTimeout(10_000);
  page.on('pageerror', error => recordErrors.push(error.message));
  page.on('console', message => {
    if (message.type() === 'error' || message.type() === 'warning') recordErrors.push(message.text());
  });
  const response = await page.goto(new URL('architecture.html', baseUrl).href, {waitUntil: 'domcontentloaded'});
  assert.equal(response.status(), 200, 'architecture page loads');
  return {context, page};
}

async function checkSearch(browser, baseUrl, assertClean) {
  const errors = [];
  const {context, page} = await openPage(browser, baseUrl, errors);
  try {
    const search = page.getByRole('searchbox', {name: 'Search documentation, commands, and versions'});
    const results = page.locator('#search-results');
    assert.equal(await search.getAttribute('aria-expanded'), 'false');
    await page.keyboard.press('/');
    assert.equal(await search.evaluate(element => document.activeElement === element), true, 'Slash focuses search');
    await search.focus();
    await search.fill('architecture');
    await results.getByRole('link', {name: /Architecture/}).first().waitFor();
    assert.equal(await search.getAttribute('aria-expanded'), 'true', 'Search announces its open state');

    await search.press('Escape');
    assert.equal(await results.isVisible(), false, 'Escape closes results');
    assert.equal(await search.inputValue(), 'architecture', 'Escape preserves the query');
    await search.press('Enter');
    assert.match(page.url(), /architecture\.html$/, 'Enter must not open hidden results');

    await search.press('ArrowDown');
    const firstResult = results.getByRole('link', {name: /Architecture/}).first();
    assert.equal(await firstResult.evaluate(element => document.activeElement === element), true, 'ArrowDown focuses results');
    await page.keyboard.press('End');
    assert.equal(await page.evaluate(() => document.activeElement === [...document.querySelectorAll('#search-results a')].at(-1)), true);
    await page.keyboard.press('Home');
    await page.keyboard.press('Escape');
    assert.equal(await results.isVisible(), false);

    await page.goto(new URL('decisions/0001-boundaries.html', baseUrl).href, {waitUntil: 'domcontentloaded'});
    await page.getByRole('searchbox', {name: 'Search documentation, commands, and versions'}).fill('architecture');
    const nestedResult = page.locator('#search-results').getByRole('link', {name: /Architecture/}).first();
    await nestedResult.waitFor();
    assert.equal(
      new URL(await nestedResult.getAttribute('href'), page.url()).href,
      new URL('architecture.html', baseUrl).href,
      'Result resolves relative to its index',
    );
    await nestedResult.click();
    assert.equal(page.url(), new URL('architecture.html', baseUrl).href, 'Nested result remains in the prefixed site');

    await assertClean(errors, 'normal search');
    return 'keyboard dismissal, query retention, nested route and hosting prefix passed';
  } finally {
    await context.close();
  }
}

async function checkIndexStates(browser, baseUrl) {
  const consoleErrors = [];
  const javascriptErrors = [];
  const {context, page} = await openPage(browser, baseUrl, consoleErrors);
  page.on('pageerror', error => javascriptErrors.push(error.message));
  try {
    let releaseResponse;
    let intercepted;
    const responsePaused = new Promise(resolve => { intercepted = resolve; });
    const responseBarrier = new Promise(resolve => { releaseResponse = resolve; });
    await page.route('**/search-index.json', async route => {
      intercepted();
      await responseBarrier;
      await route.continue();
    });
    await page.reload({waitUntil: 'domcontentloaded'});
    const search = page.getByRole('searchbox', {name: 'Search documentation, commands, and versions'});
    const results = page.locator('#search-results');
    await search.fill('architecture');
    await assert.doesNotReject(() => results.getByText('Loading search…').waitFor());
    await withTimeout(responsePaused, 'Search index request readiness');
    await search.press('Escape');
    releaseResponse();
    await page.getByRole('link', {name: /Architecture/}).first().waitFor();
    assert.equal(await results.isVisible(), false, 'A late index response respects dismissal');
    await search.press('ArrowDown');
    assert.equal(await results.isVisible(), true, 'ArrowDown reopens loaded results');
    await page.unroute('**/search-index.json');

    const cases = [
      {name: 'HTTP error', response: {status: 503, contentType: 'application/json', body: '{}'}, expected: 'Search is unavailable'},
      {name: 'malformed JSON', response: {status: 200, contentType: 'application/json', body: '{'}, expected: 'Search is unavailable'},
      {name: 'malformed entry', response: {status: 200, contentType: 'application/json', body: '{"entries":[{}]}'}, expected: 'Search is unavailable'},
      {name: 'empty index', response: {status: 200, contentType: 'application/json', body: '{"schema_version":1,"entries":[]}'}, expected: 'No pages match'},
      {name: 'legacy index', response: {status: 200, contentType: 'application/json', body: '[{"title":"Architecture","section":"Guide","text":"architecture","url":"architecture.html"}]'}, expected: 'Architecture'},
    ];
    for (const testCase of cases) {
      await page.route('**/search-index.json', route => route.fulfill(testCase.response));
      await page.goto(new URL('architecture.html', baseUrl).href, {waitUntil: 'domcontentloaded'});
      const indexSearch = page.getByRole('searchbox', {name: 'Search documentation, commands, and versions'});
      await indexSearch.fill('architecture');
      await page.locator('#search-results').getByText(testCase.expected, {exact: false}).first().waitFor();
      await page.unroute('**/search-index.json');
    }
    assert.deepEqual(javascriptErrors, [], 'Search fallback states do not cause JavaScript exceptions');
    assert.equal(consoleErrors.length, 1, 'Only the deliberately failed index request reaches the console');
    assert.match(consoleErrors[0], /503|Service Unavailable/);
    return 'delayed response, HTTP/JSON/entry failures, empty and legacy indexes passed';
  } finally {
    await context.close();
  }
}

async function checkAccessibilityAndLayouts(browser, browserName, baseUrl, browserVersion) {
  const errors = [];
  const {context, page} = await openPage(browser, baseUrl, errors);
  try {
    const headingLevels = await page.locator('main :is(h1, h2, h3, h4, h5, h6)')
      .evaluateAll(headings => headings.map(heading => Number(heading.tagName.slice(1))));
    assert.equal(headingLevels[0], 1, 'Main content starts with an h1');
    assert.equal(headingLevels.filter(level => level === 1).length, 1, 'Page has one main heading');
    for (let index = 1; index < headingLevels.length; index++) {
      assert(headingLevels[index] <= headingLevels[index - 1] + 1, 'Heading levels do not skip a level');
    }
    assert.equal(await page.locator('main img').evaluateAll(images => images.every(image => image.alt.trim())), true, 'Images have descriptions');
    assert.equal(await page.locator('#search-results').getAttribute('aria-live'), 'polite');
    assert.equal(await page.getByRole('link', {name: 'Skip to content'}).count(), 1, 'Skip link has an accessible name');
    const style = page.getByRole('combobox', {name: 'Documentation visual theme'});
    const mode = page.getByRole('combobox', {name: 'Colour theme'});
    const version = page.getByRole('combobox', {name: 'Documentation version'});
    assert.equal(await style.count(), 1);
    assert.equal(await mode.count(), 1);
    assert.equal(await version.count(), 1);
    const inlineOutline = page.locator('.inline-toc');
    const inlineSummary = inlineOutline.locator(':scope > summary');
    await style.focus();
    await page.keyboard.press('ArrowDown');
    assert.equal(await style.inputValue(), 'paper', 'Style control works with ArrowDown');
    await page.keyboard.press('Home');
    assert.equal(await style.inputValue(), 'classic', 'Style control works with Home');
    await mode.focus();
    await page.keyboard.press('End');
    assert.equal(await mode.inputValue(), 'dark', 'Colour mode works with End');
    await page.keyboard.press('Home');
    assert.equal(await mode.inputValue(), 'system', 'Colour mode works with Home');
    await page.goto(new URL('architecture.html', baseUrl).href, {waitUntil: 'domcontentloaded'});

    const initialFocus = await page.evaluate(() => ({tag: document.activeElement.tagName, id: document.activeElement.id}));
    await page.keyboard.press('Tab');
    const firstFocus = await page.evaluate(() => ({
      tag: document.activeElement.tagName,
      id: document.activeElement.id,
      className: typeof document.activeElement.className === 'string' ? document.activeElement.className : '',
    }));
    assert(firstFocus.className.split(/\s+/).includes('skip-link'), `First Tab should reach skip link from ${JSON.stringify(initialFocus)}; got ${JSON.stringify(firstFocus)}`);
    assert.notEqual(await page.evaluate(() => getComputedStyle(document.activeElement).outlineStyle), 'none', 'Skip link focus is visible');
    await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'content', 'Skip link moves focus to article');
    await page.keyboard.press('Tab');
    const firstControl = await page.evaluate(() => ({tag: document.activeElement.tagName, id: document.activeElement.id}));
    assert(
      ['A', 'BUTTON', 'INPUT', 'SELECT', 'SUMMARY', 'BODY'].includes(firstControl.tag),
      `Tab leaves the article or advances to a control; got ${JSON.stringify(firstControl)}`,
    );

    const mobileNavigation = page.locator('.mobile-nav');
    for (const width of [320, 768, 1024, 1440]) {
      await page.setViewportSize({width, height: 1000});
      for (const theme of ['classic', 'paper', 'e-ink', 'glassmorphic']) {
        for (const mode of ['light', 'dark']) {
          await page.emulateMedia({colorScheme: mode});
          await page.locator('#visual-theme').selectOption(theme);
          await page.locator('#theme-select').selectOption(mode);
          const diagram = page.locator('main img[src$="build-pipeline.svg"]');
          await diagram.scrollIntoViewIfNeeded();
          await page.waitForFunction(() => {
            const image = document.querySelector('main img[src$="build-pipeline.svg"]');
            return image?.complete && image.naturalWidth > 0;
          });
          const observed = await page.evaluate(() => ({
            width: innerWidth,
            overflow: document.documentElement.scrollWidth > innerWidth,
            theme: document.documentElement.dataset.visualTheme,
            mode: document.documentElement.dataset.theme,
          }));
          assert.equal(observed.overflow, false, `${browserName}/${width}/${theme}/${mode}: horizontal overflow`);
          assert.equal(observed.theme, theme);
          assert.equal(observed.mode, mode);
          assert(await diagram.evaluate(image => image.complete && image.naturalWidth > 0), `${browserName}: diagram loads`);
          const measuredWidth = await diagram.evaluate(image => image.getBoundingClientRect().width);
          assert(measuredWidth <= width, `${browserName}/${width}: diagram fits the viewport`);
      if (width <= 1024) {
        assert.equal((await inlineSummary.textContent()).trim(), 'On this page', 'Inline outline has a visible name');
        await inlineSummary.focus();
        await page.keyboard.press('Enter');
        assert.equal(await inlineOutline.evaluate(outline => outline.open), true, `${browserName}/${width}: keyboard opens the page outline`);
        await page.keyboard.press('Enter');
        assert.equal(await inlineOutline.evaluate(outline => outline.open), false, `${browserName}/${width}: keyboard closes the page outline`);
      }
      assert.equal(await inlineOutline.evaluate(outline => outline.open), false, 'Scrolling preserves closed outline');
          results.push({browser: browserName, version: browserVersion, width, theme, mode, passed: true});
          if ([320, 1440].includes(width) && ['classic', 'paper'].includes(theme)) {
            const imageName = `${browserName}-${width}-${theme}-${mode}.png`;
            await page.screenshot({path: path.join(artifactsDirectory, imageName), fullPage: true});
          }
          if ([320, 1440].includes(width) && theme === 'classic' && mode === 'light') {
            await diagram.screenshot({path: path.join(artifactsDirectory, `${browserName}-diagram-${width}.png`)});
          }
        }
      }
      if (width <= 768) {
        const summary = mobileNavigation.locator(':scope > summary');
        assert.equal((await summary.textContent()).trim(), 'Browse documentation', 'Mobile navigation has a visible name');
        await summary.focus();
        await page.keyboard.press('Enter');
        assert.equal(await mobileNavigation.evaluate(details => details.open), true, `${browserName}/${width}: keyboard opens navigation`);
        await page.keyboard.press('Enter');
        assert.equal(await mobileNavigation.evaluate(details => details.open), false, `${browserName}/${width}: keyboard closes navigation`);
      }
    }
    await context.clearCookies();
    await page.emulateMedia({media: 'print'});
    assert.equal(await page.locator('.toc').isVisible(), false, 'Print hides screen navigation');
    await assertClean(errors, `${browserName} layout matrix`);
    return 'accessible structure, focus order, disclosure and 32 responsive theme cases passed';
  } finally {
    await context.close();
  }
}

async function assertClean(errors, description) {
  assert.deepEqual(errors, [], `${description} should produce a clean browser console`);
}

await mkdir(artifactsDirectory, {recursive: true});
let server;
try {
  if (requestedBrowser && !Object.hasOwn(browsers, requestedBrowser)) {
    throw new Error(`Unknown browser ${requestedBrowser}; choose chromium, firefox or webkit`);
  }
  await buildSite();
  const served = await serveSite();
  server = served.server;
  const {baseUrl} = served;
  for (const [browserName, engine] of Object.entries(browsers).filter(([name]) => !requestedBrowser || name === requestedBrowser)) {
    const logFile = path.join(artifactsDirectory, `${browserName}.log`);
    try {
      const browser = await engine.launch({headless: true, timeout: 30_000});
      try {
        const browserVersion = browser.version();
        const checks = [
          await checkSearch(browser, baseUrl, assertClean),
          await checkIndexStates(browser, baseUrl),
          await checkAccessibilityAndLayouts(browser, browserName, baseUrl, browserVersion),
        ];
        results.push({browser: browserName, version: browserVersion, checks});
        const message = `${browserName} ${browserVersion}: ${checks.join('; ')}`;
        console.log(message);
        await writeFile(logFile, `${message}\n`, 'utf8');
      } finally {
        await browser.close();
      }
    } catch (error) {
      const message = `${browserName}: ${error.stack || error.message}`;
      await writeFile(logFile, `${message}\n`, 'utf8');
      throw new Error(`${message}\nIf the browser is missing, run: npx playwright install ${browserName}`, {cause: error});
    }
  }
} catch (error) {
  failure = error;
  const message = error.stack || error.message;
  await writeFile(path.join(artifactsDirectory, 'run.log'), `${message}\n`, 'utf8');
  console.error(message);
  process.exitCode = 1;
} finally {
  if (server) {
    try {
      await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    } catch (error) {
      failure ??= error;
      process.exitCode = 1;
      console.error(`Server cleanup failed: ${error.stack || error.message}`);
    }
  }
  await writeFile(path.join(artifactsDirectory, 'results.json'), `${JSON.stringify({
    node: process.version,
    browser: requestedBrowser || 'all',
    results,
    failure: failure?.message,
  }, null, 2)}\n`, 'utf8');
}
