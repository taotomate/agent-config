import { chromium } from 'playwright';

async function extractTranscript(videoUrl: string) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log(`Navegando a: ${videoUrl}`);
    await page.goto(videoUrl, { waitUntil: 'networkidle' });

    // 0. Limpieza agresiva de overlays (Cookies/Consentimiento)
    console.log('Limpiando posibles bloqueos de UI...');
    await page.evaluate(() => {
        const selectors = [
            'ytd-consent-bump-v2-lightbox',
            'tp-yt-paper-dialog',
            '.opened',
            'iron-overlay-backdrop'
        ];
        selectors.forEach(s => {
            const el = document.querySelector(s);
            if (el) el.remove();
        });
        // Habilitar scroll por si lo bloquearon
        document.body.style.overflow = 'auto';
    });
    await page.waitForTimeout(500);

    // 1. Expandir descripción
    console.log('Expandiendo descripción...');
    const expandButton = page.locator('ytd-text-inline-expander #expand, #expand').first();
    // Forzamos el click si es necesario
    await expandButton.click({ force: true }).catch(() => console.log('No se pudo clickear expandir (quizás ya expandido o no existe)'));
    await page.waitForTimeout(1000);

    // 2. Abrir panel de transcripción
    console.log('Buscando botón de transcripción...');
    const transcriptButton = page.locator('ytd-video-description-transcript-section-renderer button').first();
    
    await transcriptButton.waitFor({ state: 'attached', timeout: 5000 });
    await transcriptButton.click({ force: true });

    // 3. Extrayendo segmentos
    console.log('Extrayendo segmentos...');
    await page.waitForSelector('transcript-segment-view-model, ytd-transcript-segment-renderer', { timeout: 10000 });

    const segments = await page.evaluate(() => {
      const results: { time: string; text: string }[] = [];
      
      let items = document.querySelectorAll('transcript-segment-view-model');
      if (items.length > 0) {
          items.forEach((item) => {
            const time = (item as HTMLElement).querySelector('div')?.innerText.trim() || '';
            const text = (item as HTMLElement).querySelector('span[role="text"]')?.innerText.trim() || '';
            if (text) results.push({ time, text });
          });
      } else {
          items = document.querySelectorAll('ytd-transcript-segment-renderer');
          items.forEach((item) => {
            const time = (item as HTMLElement).querySelector('.segment-timestamp')?.textContent?.trim() || '';
            const text = (item as HTMLElement).querySelector('.segment-text')?.textContent?.trim() || '';
            if (text) results.push({ time, text });
          });
      }
      return results;
    });

    console.log(JSON.stringify(segments, null, 2));
    
  } catch (error) {
    console.error('Error al extraer transcripción:', error);
  } finally {
    await browser.close();
  }
}

const url = process.argv[2];
if (!url) {
  console.error('Uso: npx tsx extract.ts <youtube-url>');
  process.exit(1);
}

extractTranscript(url);
