const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({
    viewport: { width: +(process.argv[4] || 1080), height: +(process.argv[5] || 1920) },
  });
  await p.goto("file://" + process.argv[2]);
  await p.waitForTimeout(500);
  await p.screenshot({ path: process.argv[3], omitBackground: true });
  await b.close();
})();
