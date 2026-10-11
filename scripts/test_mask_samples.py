import os
import sys
from playwright.sync_api import sync_playwright

def test_mask_samples():
    html_path = os.path.abspath("studio.html")
    url = f"file:///{html_path.replace(os.sep, '/')}#mask"
    print(f"Testing URL: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: console_logs.append(f"[ERROR] {err}"))
        
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(500)
        
        # 1. Verify drop zone has sample buttons
        sample_btns = page.locator(".sample-btn").all()
        print(f"Found {len(sample_btns)} sample buttons on page.")
        assert len(sample_btns) >= 2, "Expected at least 2 sample buttons!"
        
        # 2. Click 1080x1920 sample button
        print("Clicking 1080x1920 sample button...")
        page.locator("button.sample-btn:has-text('1080×1920')").first.click()
        page.wait_for_timeout(800)
        
        # Check canvas visibility and status text
        status_text = page.locator("#mask-status-text").inner_text()
        print(f"Mask status after 1080x1920: {status_text}")
        assert "1080x1920" in status_text, f"Expected 1080x1920 in status, got: {status_text}"
        
        # Screenshot 1
        page.screenshot(path="samples/test_1080x1920_loaded.png")
        print("Saved samples/test_1080x1920_loaded.png")
        
        # 3. Simulate drawing on canvas
        draw_canvas = page.locator("#draw-canvas")
        box = draw_canvas.bounding_box()
        if box:
            print(f"Canvas box: {box}")
            start_x = box["x"] + box["width"] * 0.3
            start_y = box["y"] + box["height"] * 0.4
            page.mouse.move(start_x, start_y)
            page.mouse.down()
            page.mouse.move(start_x + 100, start_y + 100)
            page.mouse.up()
            page.wait_for_timeout(300)
            print("Drawn test mask rectangle.")
        
        # Screenshot 2 with drawn mask
        page.screenshot(path="samples/test_1080x1920_drawn.png")
        print("Saved samples/test_1080x1920_drawn.png")
        
        # 4. Click 1080x1350 sample button in control panel
        print("Clicking 1080x1350 sample button...")
        page.locator(".mask-sample-bar button.sample-btn:has-text('1080×1350')").click()
        page.wait_for_timeout(800)
        
        status_text_2 = page.locator("#mask-status-text").inner_text()
        print(f"Mask status after 1080x1350: {status_text_2}")
        assert "1080x1350" in status_text_2, f"Expected 1080x1350 in status, got: {status_text_2}"
        
        # Screenshot 3
        page.screenshot(path="samples/test_1080x1350_loaded.png")
        print("Saved samples/test_1080x1350_loaded.png")
        
        # 5. Clear mask
        print("Testing Clear Mask...")
        page.locator("#btn-clear-mask").click()
        page.wait_for_timeout(500)
        
        # Print console logs
        print("\n--- BROWSER CONSOLE LOGS ---")
        for log in console_logs:
            print(log)
            
        errors = [l for l in console_logs if "[ERROR]" in l or "[error]" in l]
        if errors:
            print(f"WARNING: Encountered {len(errors)} browser errors:")
            for err in errors:
                print("  ", err)
        else:
            print("ALL BROWSER TESTS PASSED WITH 0 ERRORS!")
            
        browser.close()

if __name__ == "__main__":
    test_mask_samples()
