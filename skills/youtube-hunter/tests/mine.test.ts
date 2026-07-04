import { describe, it, expect } from 'vitest';
import { extractTranscriptUrl, mapJson3ToFormat } from '../scripts/transcript-api';

/**
 * Mock of the ytInitialPlayerResponse structure we expect to find in the page.
 */
export const mockPlayerResponse = {
    captions: {
        playerCaptionsTracklistRenderer: {
            captionTracks: [
                {
                    baseUrl: 'https://www.youtube.com/api/timedtext?v=abc&fmt=json3',
                    name: { simpleText: 'English' },
                    languageCode: 'en'
                }
            ]
        }
    },
    videoDetails: {
        title: 'Test Video Title',
        author: 'Test Channel',
        lengthSeconds: '120'
    }
};

/**
 * Mock of the JSON3 transcript format returned by YouTube.
 */
export const mockJson3Transcript = {
    events: [
        { tStartMs: 0, dDurationMs: 1000, segs: [{ utf8: 'Hello' }] },
        { tStartMs: 1000, dDurationMs: 2000, segs: [{ utf8: 'world' }] }
    ]
};

describe('YouTube Hunter - Transcript API Logic', () => {
    it('should extract the correct transcript URL from player response', () => {
        const url = extractTranscriptUrl(mockPlayerResponse as any);
        expect(url).toBe('https://www.youtube.com/api/timedtext?v=abc&fmt=json3');
    });

    it('should map JSON3 segments to the [MM:SS] text format', () => {
        const formatted = mapJson3ToFormat(mockJson3Transcript as any);
        expect(formatted).toBe('[00:00] Hello\n[00:01] world');
    });
});
