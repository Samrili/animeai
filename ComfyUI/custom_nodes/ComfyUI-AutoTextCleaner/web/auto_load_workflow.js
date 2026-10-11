import { app } from "../../scripts/app.js";

const TAB_ID = "animeai_tab_" + Math.random().toString(36).substring(2, 9) + "_" + Date.now();
const BROADCAST_CHANNEL_NAME = "animeai_session_channel";

// Multi-tab sync channel: Deactivate obsolete tabs when a new session starts
let sessionChannel = null;
try {
    sessionChannel = new BroadcastChannel(BROADCAST_CHANNEL_NAME);
    sessionChannel.onmessage = (event) => {
        const data = event.data;
        if (data && data.type === "NEW_SESSION_LAUNCHED" && data.tabId !== TAB_ID) {
            console.warn("[AnimeAI] Yeni bir oturum baslatildi, bu eski sekme pasife aliniyor.");
            deactivateOldTab(data.timestamp);
        }
    };
} catch (e) {
    console.log("[AnimeAI] BroadcastChannel not supported in this browser environment:", e);
}

function deactivateOldTab(timestamp) {
    // 1. Durdurulmus tum videolari ve sesleri sustur
    document.querySelectorAll("video, audio").forEach(el => {
        try {
            el.pause();
            el.src = "";
            el.load();
        } catch (err) {}
    });

    // 2. LiteGraph cizim dongusunu durdur
    if (app && app.canvas) {
        try {
            app.canvas.stopRendering?.();
        } catch (err) {}
    }

    // 3. Kullaniciyi bilgilendirici tam ekran overlay goster
    const existingOverlay = document.getElementById("animeai-obsolete-overlay");
    if (existingOverlay) return;

    const overlay = document.createElement("div");
    overlay.id = "animeai-obsolete-overlay";
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100vw";
    overlay.style.height = "100vh";
    overlay.style.backgroundColor = "rgba(10, 10, 18, 0.94)";
    overlay.style.backdropFilter = "blur(10px)";
    overlay.style.zIndex = "9999999";
    overlay.style.display = "flex";
    overlay.style.flexDirection = "column";
    overlay.style.alignItems = "center";
    overlay.style.justifyContent = "center";
    overlay.style.fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    overlay.style.color = "#ffffff";
    overlay.style.textAlign = "center";
    overlay.style.padding = "24px";

    overlay.innerHTML = `
        <div style="background: rgba(26, 26, 38, 0.95); border: 1px solid rgba(255, 38, 70, 0.4); border-radius: 16px; padding: 36px 48px; max-width: 520px; box-shadow: 0 20px 50px rgba(0,0,0,0.8);">
            <div style="font-size: 13px; font-weight: 700; color: #ff3b5c; letter-spacing: 1.5px; margin-bottom: 12px; text-transform: uppercase;">Oturum Durumu</div>
            <h2 style="margin: 0 0 12px 0; font-size: 22px; font-weight: 700; color: #ffffff;">Eski AnimeAI Sekmesi Durduruldu</h2>
            <p style="margin: 0 0 20px 0; color: #a1a1aa; font-size: 14px; line-height: 1.6;">
                Yeni bir <b>baslat.bat</b> oturumu calistirildi ve yeni sekme acildi.<br>
                GPU bellegini (VRAM) korumak ve cakisikliklari onlemek icin bu eski sekme guvenle durdurulmustur.
            </p>
            <div style="display: flex; gap: 12px; justify-content: center;">
                <button id="animeai-close-tab-btn" style="background: #ff2646; color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s;">
                    Bu Sekmeyi Kapat
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);
    const closeBtn = document.getElementById("animeai-close-tab-btn");
    if (closeBtn) {
        closeBtn.onclick = () => {
            window.close();
            // Eger browser window.close'a izin vermezse
            overlay.innerHTML = `<h2 style="color: #ff3b5c;">Lutfen bu tarayici sekmesini carpidan kapatiniz.</h2>`;
        };
    }
}

function showNotificationToast(msg) {
    const existing = document.getElementById("animeai-toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.id = "animeai-toast";
    toast.style.position = "fixed";
    toast.style.top = "18px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.backgroundColor = "rgba(18, 18, 28, 0.95)";
    toast.style.border = "1px solid rgba(139, 92, 246, 0.6)";
    toast.style.borderRadius = "30px";
    toast.style.padding = "10px 22px";
    toast.style.color = "#ffffff";
    toast.style.fontSize = "13px";
    toast.style.fontWeight = "600";
    toast.style.zIndex = "999999";
    toast.style.boxShadow = "0 8px 30px rgba(0, 0, 0, 0.6)";
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.gap = "10px";
    toast.style.pointerEvents = "none";
    toast.style.animation = "animeaiFadeIn 0.3s ease-out";

    toast.innerHTML = `
        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
        <span>${msg}</span>
    `;

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = "opacity 0.5s ease-out";
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

app.registerExtension({
    name: "AnimeAI.AutoWorkflowLoader",
    async setup() {
        console.log("[AnimeAI] AutoWorkflowLoader extension initializing...");

        // VHS Video Önizleme ayarını (videoyu kısaltma & FPS düşürmeyi anlık göstermesi için) etkinleştir
        try {
            if (app.ui?.settings) {
                const advSetting = app.ui.settings.getSettingValue("VHS.AdvancedPreviews");
                if (!advSetting || advSetting === "Never") {
                    console.log("[AnimeAI] VHS.AdvancedPreviews 'Input Only' olarak etkinlestiriliyor...");
                    app.ui.settings.setSettingValue("VHS.AdvancedPreviews", "Input Only");
                }
            }
        } catch (e) {
            console.warn("[AnimeAI] VHS.AdvancedPreviews ayari kontrol edilemedi:", e);
        }

        async function closeOtherWorkflowTabs() {
            try {
                // Modern ComfyUI workflow tab bar temizligi
                const tabCloseButtons = document.querySelectorAll(".workflow-tab .pi-times, .workflow-tab [data-action='close']");
                if (tabCloseButtons && tabCloseButtons.length > 1) {
                    console.log(`[AnimeAI] ${tabCloseButtons.length} adet diger workflow sekmesi kapatiliyor...`);
                    for (let i = 1; i < tabCloseButtons.length; i++) {
                        tabCloseButtons[i].click?.();
                    }
                }
                // LocalStorage'daki diger acik tab yollarini sifirla
                localStorage.removeItem("Comfy.OpenWorkflowsPaths");
                localStorage.removeItem("Comfy.ActiveWorkflowIndex");
            } catch (err) {
                console.warn("[AnimeAI] Tab temizleme hatasi (onemsiz):", err);
            }
        }

        async function loadOptimizedWorkflow(force = false) {
            try {
                let info = null;
                try {
                    const infoResp = await fetch("/animeai/info");
                    if (infoResp.ok) {
                        info = await infoResp.json();
                    }
                } catch (e) {
                    console.warn("[AnimeAI] /animeai/info ulasilamadi:", e);
                }

                const lastServerId = localStorage.getItem("animeai_last_server_id");
                const isNewServerLaunch = info && info.server_id && (info.server_id !== lastServerId);

                const currentNodes = app.graph?._nodes || [];
                const hasOldVAE = currentNodes.some(n => n.type === "VAEDecodeTiled");
                const hasBatchedVAE = currentNodes.some(n => n.type === "VHS_VAEDecodeBatched");
                const isAnimeAIWorkflow = currentNodes.some(n => n.type === "AutoTextCleaner" || n.type === "AutoTextShapeOverlay");

                const shouldLoad = force || isNewServerLaunch || hasOldVAE || !hasBatchedVAE || !isAnimeAIWorkflow || currentNodes.length === 0;

                if (shouldLoad) {
                    console.log("[AnimeAI] Guncel ve hizli AnimeAI workflowu (Batched VAE + NVENC) yukleniyor...");
                    
                    // Diger sekmeleri ve taslaklari kapat
                    await closeOtherWorkflowTabs();

                    const resp = await fetch("/animeai/workflow");
                    if (resp.ok) {
                        const workflow = await resp.json();
                        
                        // Aktif grafi temizle ve dogru workflowu yukle
                        if (app.graph) {
                            app.graph.clear();
                        }
                        await app.loadGraphData(workflow);

                        if (info && info.server_id) {
                            localStorage.setItem("animeai_last_server_id", info.server_id);
                        }

                        // Sekme basligini belirle
                        document.title = "AnimeAI Studio (Hazir - Hizli Akis)";

                        // Ekrani baslangic dugumlerine odakla
                        setTimeout(() => {
                            try {
                                if (app.canvas) {
                                    app.canvas.fitContent?.();
                                }
                            } catch (e) {}
                        }, 400);

                        showNotificationToast("AnimeAI Hizli Akisi Yuklendi (NVENC + Batched VAE)");

                        // Diger tum eski tarayici sekmelerine haber ver
                        if (sessionChannel) {
                            sessionChannel.postMessage({
                                type: "NEW_SESSION_LAUNCHED",
                                tabId: TAB_ID,
                                timestamp: Date.now()
                            });
                        }
                    } else {
                        console.error("[AnimeAI] /animeai/workflow dosyasi alinamadi, HTTP:", resp.status);
                    }
                } else {
                    console.log("[AnimeAI] Tuval zaten guncel optimize akisa sahip.");
                }
            } catch (err) {
                console.error("[AnimeAI] Workflow yukleme sirasinda hata olustu:", err);
            }
        }

        // ComfyUI ilk acildiginda calistir
        setTimeout(() => {
            loadOptimizedWorkflow(false);
        }, 600);

        // Kullanicinin istedigi zaman tek tikla akisi tazeleyebilmesi icin menu butonu
        const menu = document.querySelector(".comfy-menu");
        if (menu) {
            const btn = document.createElement("button");
            btn.textContent = "AnimeAI Hizli Akisi Yukle";
            btn.title = "Dogru ve optimize akisi yukler, digerlerini temizler";
            btn.style.background = "linear-gradient(135deg, #ff2646, #8b5cf6)";
            btn.style.color = "#ffffff";
            btn.style.fontWeight = "bold";
            btn.style.fontSize = "12px";
            btn.style.border = "1px solid rgba(255,255,255,0.3)";
            btn.style.borderRadius = "6px";
            btn.style.padding = "6px 12px";
            btn.style.cursor = "pointer";
            btn.style.margin = "4px 0";
            btn.onclick = () => {
                loadOptimizedWorkflow(true);
            };
            menu.insertBefore(btn, menu.firstChild);
        }
    }
});
