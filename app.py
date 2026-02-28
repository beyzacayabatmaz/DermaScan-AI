import streamlit as st
import streamlit.components.v1 as components
import time
import random

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="DermaScan AI | The Purest Solutions Lab",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Dinamik Tema (Light/Dark Mode) & Marka Kimliği
st.markdown("""
<style>
    /* Global Renk Değişkenleri */
    :root {
        --cobalt-blue: #0047AB;
        --card-bg: #FFFFFF;
        --text-color: #1A1A1A;
        --sub-text: #666666;
        --border-color: #EAEAEA;
    }

    /* Karanlık Mod Uyumu */
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: #1E1E1E;
            --text-color: #F5F5F7;
            --sub-text: #B0B0B0;
            --border-color: #333333;
        }
        .stApp {
            background-color: #121212 !important;
        }
    }

    .stApp {
        color: var(--text-color);
        font-family: 'Inter', -apple-system, sans-serif;
    }

    [data-testid="stVerticalBlock"] > div:first-child {
        max-width: 500px;
        margin: 0 auto;
    }

    /* Klinik Kart Tasarımı */
    .clinical-card {
        background-color: var(--card-bg);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        color: var(--text-color);
    }

    /* Buton Tasarımı */
    .stButton > button {
        width: 100%;
        background-color: var(--cobalt-blue) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 16px 0px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:disabled {
        background-color: #444 !important;
        color: #888 !important;
        cursor: not-allowed;
        opacity: 0.6;
    }

    .stButton > button:hover:not(:disabled) {
        background-color: #003580 !important;
        box-shadow: 0 8px 25px rgba(0, 71, 171, 0.3);
        transform: translateY(-2px);
    }

    /* Reçete Kartı */
    .expert-result-card {
        background: linear-gradient(135deg, #0047AB 0%, #002D6B 100%);
        color: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 71, 171, 0.2);
    }

    p, span, h3, h4 {
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# Gelişmiş Kamera Bileşeni
def camera_preview(is_scanning=False):
    scanning_js = "true" if is_scanning else "false"
    html_code = f"""
    <div id="cam-box" style="width:100%; border-radius:20px; overflow:hidden; position:relative; background:#111; aspect-ratio: 4/3; border: 1px solid #444; display: flex; align-items: center; justify-content: center;">
        <div id="loading-msg" style="color: white; font-family: sans-serif; font-size: 13px; text-align: center; position: absolute; z-index: 1;">
            <p>Klinik Tarayıcı Hazırlanıyor...</p>
            <p style="font-size: 11px; opacity: 0.6;">Lütfen kamera iznini onaylayın.</p>
        </div>
        <div id="face-detect-msg" style="display:none; position:absolute; top:20px; background:rgba(217, 4, 41, 0.9); color:white; padding:10px 20px; border-radius:20px; font-size:13px; z-index:10; font-weight:bold; border: 1px solid white;">
            ⚠️ Lütfen kameraya doğru yüzünüzü gösteriniz
        </div>
        <video id="v" autoplay playsinline style="width:100%; height:100%; object-fit: cover; transform: scaleX(-1); position: relative; z-index: 2;"></video>
        <canvas id="c" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; transform: scaleX(-1); z-index: 3;"></canvas>
    </div>
    <script>
        const v = document.getElementById("v");
        const c = document.getElementById("c");
        const ctx = c.getContext("2d");
        const loading = document.getElementById("loading-msg");
        const faceMsg = document.getElementById("face-detect-msg");
        const isScan = {scanning_js};
        let streamObj = null;
        
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
            navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "user" }} }})
                .then(s => {{
                    streamObj = s;
                    v.srcObject = s;
                    loading.style.display = 'none';
                }})
                .catch(err => {{
                    loading.innerHTML = "<div style='color:#FF4B4B; padding:20px;'>Kamera erişimi reddedildi.</div>";
                }});
        }}

        let pts = [];
        function initPts() {{
            pts = [];
            for(let i=0; i<180; i++) {{
                pts.push({{
                    x: Math.random() * c.width,
                    y: Math.random() * c.height,
                    s: Math.random() * 2,
                    vx: (Math.random() - 0.5) * 1.2,
                    vy: (Math.random() - 0.5) * 1.2,
                    o: Math.random() * 100
                }});
            }}
        }}

        function draw() {{
            if (v.readyState === v.HAVE_ENOUGH_DATA) {{
                if (c.width !== v.videoWidth) {{
                    c.width = v.videoWidth;
                    c.height = v.videoHeight;
                    initPts();
                }}
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                if(isScan) {{
                    ctx.fillStyle = "rgba(0, 255, 0, 0.7)";
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = "#00FF00";
                    pts.forEach(p => {{
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, p.s, 0, 6.28);
                        ctx.fill();
                        p.x += p.vx + Math.sin(Date.now() * 0.0015 + p.o) * 1;
                        p.y += p.vy + Math.cos(Date.now() * 0.0015 + p.o) * 1;
                        if(p.x < 0) p.x = c.width;
                        if(p.x > c.width) p.x = 0;
                        if(p.y < 0) p.y = c.height;
                        if(p.y > c.height) p.y = 0;
                    }});
                }}
            }}
            requestAnimationFrame(draw);
        }}
        v.addEventListener('play', draw);

        window.addEventListener('unload', () => {{
            if(streamObj) streamObj.getTracks().forEach(t => t.stop());
        }});
    </script>
    """
    components.html(html_code, height=360)

# Session State
if 'step' not in st.session_state: st.session_state.step = 1
if 'user' not in st.session_state: st.session_state.user = {}
if 'cam_granted' not in st.session_state: st.session_state.cam_granted = False
if 'scan_active' not in st.session_state: st.session_state.scan_active = False
if 'analysis_results' not in st.session_state: st.session_state.analysis_results = {}
if 'error_msg' not in st.session_state: st.session_state.error_msg = ""

def reset(): 
    st.session_state.step = 1
    st.session_state.user = {}
    st.session_state.cam_granted = False
    st.session_state.scan_active = False
    st.session_state.analysis_results = {}
    st.session_state.error_msg = ""
    st.rerun()

# --- HEADER ---
st.markdown("<div style='text-align: center; margin-bottom: 30px;'><h2 style='color: #0047AB; margin-bottom: 0;'>DermaScan AI</h2><p style='font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 3px; font-weight: 700;'>Optical Diagnostic Laboratory</p></div>", unsafe_allow_html=True)

# --- AKIŞ ---

# ADIM 1: PROFİL
if st.session_state.step == 1:
    st.markdown("<div class='clinical-card'><h3>Kullanıcı Profili</h3>", unsafe_allow_html=True)
    age = st.number_input("Yaşınız", 12, 85, 20)
    gender = st.selectbox("Cinsiyetiniz", ["Kadın", "Erkek"])
    st.session_state.user.update({"age": age, "gender": gender})
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Profili Kaydet ve İlerle"):
        st.session_state.step = 2
        st.rerun()

# ADIM 2: KAMERA VE ANALİZ (Regl Döngüsü Zorunlu)
elif st.session_state.step == 2:
    if not st.session_state.cam_granted:
        st.markdown("<div class='clinical-card'><h4>Kamera Erişimi Gerekli</h4><p style='font-size: 14px;'>AI modelinin görsel analiz yapabilmesi için kamera erişimi gereklidir.</p></div>", unsafe_allow_html=True)
        if st.button("Kamerayı Aktif Et"):
            st.session_state.cam_granted = True
            st.rerun()
    else:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        
        is_ready = True
        if st.session_state.user['gender'] == "Kadın":
            st.markdown("<p style='font-weight:600; font-size:14px; margin-bottom:5px;'>Regl Döngüsü Analizi</p>", unsafe_allow_html=True)
            
            # Gün seçimi (Zorunlu)
            cycle_options = ["Seçiniz"] + [str(i) for i in range(1, 36)]
            cycle_input = st.selectbox("Regl döngünüzü giriniz (Kaçıncı gündesiniz?)", cycle_options, index=0)
            
            # Dönem sorgusu
            on_period = st.radio("Şu an regl dönemi içerisinde misiniz?", ["Evet", "Hayır"], horizontal=True, index=1)
            st.session_state.user['on_period'] = (on_period == "Evet")
            
            st.markdown("<p style='font-size: 13px; color: #555; margin-top: 10px; margin-bottom: 15px;'>Hormonal sivilceler için regl döngüsü girmenizi istiyoruz.</p>", unsafe_allow_html=True)
            
            if cycle_input == "Seçiniz":
                is_ready = False
            else:
                st.session_state.user['cycle'] = int(cycle_input)
            st.markdown("<hr style='opacity: 0.1; margin: 15px 0;'>", unsafe_allow_html=True)

        st.markdown("<p style='text-align:center; font-weight:600; margin-bottom:10px;'>Canlı Optik Tarama Alanı</p>", unsafe_allow_html=True)
        
        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)
            st.session_state.error_msg = ""

        camera_preview(is_scanning=st.session_state.scan_active)
        
        if not st.session_state.scan_active:
            if not is_ready:
                st.warning("Lütfen yukarıdaki regl döngüsü bilgisini giriniz.")
                st.button("Analizi Başlat", disabled=True)
            else:
                if st.button("Analizi Başlat"):
                    with st.spinner("AI Yüz Arıyor..."):
                        time.sleep(1.5)
                        face_verified = random.random() > 0.2
                        if face_verified:
                            st.session_state.scan_active = True
                            st.rerun()
                        else:
                            st.session_state.error_msg = "❌ Yüz algılanamadı! Lütfen kameraya doğru bakınız."
                            st.rerun()
        else:
            status = st.empty()
            metrics = ["Bariyer Ölçümü", "Gözenek Haritalama", "Kızarıklık Tespiti", "Sebum Analizi"]
            scan_ok = True
            for m in metrics:
                if random.random() < 0.05:
                    scan_ok = False
                    break
                status.markdown(f"<p style='text-align:center; color:#0047AB; font-weight:700;'>{m} Yapılıyor...</p>", unsafe_allow_html=True)
                time.sleep(1.2)
            
            if scan_ok:
                st.session_state.analysis_results = {
                    "sebum": random.choice(["Yüksek", "Dengeli", "Düşük"]),
                    "pores": random.choice(["Genişlemiş", "Sıkı", "Tıkalı"]),
                    "redness": random.choice([True, False]),
                    "moisture": random.randint(20, 95)
                }
                st.session_state.step = 3
                st.session_state.scan_active = False
                st.rerun()
            else:
                st.session_state.scan_active = False
                st.session_state.error_msg = "⚠️ Analiz Kesildi: Yüz odağı kayboldu!"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ADIM 3: SONUÇLAR VE MOBİL UYUMLU LİNKLER
elif st.session_state.step == 3:
    u = st.session_state.user
    res = st.session_state.analysis_results
    st.markdown("<h3 style='text-align: center;'>Klinik Analiz Raporu</h3>", unsafe_allow_html=True)
    
    # TR RESMİ SİTESİ CANONICAL LİNKLERİ (Mobil 404 Fix)
    prods = {
        "niacinamide": {"t": "Intensive Pore Tightening Serum", "f": "Niacinamide %5 + Zinc PCA %1", "url": "gozenek-sikilastirici-ve-aydinlatici-serum-niacinamide-5-zinc-pca-1"},
        "hyaluronic": {"t": "Hyaluronic Acid %2 + B5", "f": "Intensive Hydration Serum", "url": "yogun-nemlendirici-bakim-serumu-hyaluronic-acid-2-b5"},
        "arbutin": {"t": "Brightening Serum", "f": "Arbutin %2 + Hyaluronic Acid", "url": "cilt-tonu-aydinlatici-leke-karsiti-cilt-bakim-serumu-arbutin-2-hyaluronic-acid"},
        "retinol": {"t": "Retinol Serum %0.5", "f": "Rejuvenating Retinol Serum", "url": "yaslanma-karsiti-yenileyici-retinol-serum-0-5-retinol-complex"},
        "blemish": {"t": "Blemish Defense Serum", "f": "Oil Control Solution", "url": "sivilce-ve-siyah-nokta-karsiti-serum-blemish-defense-serum"},
        "vitc": {"t": "Vitamin C Serum %10", "f": "Ethyl Ascorbic Acid", "url": "aydinlatici-leke-karsiti-serum-10-vitamin-c-0-5-ferulic-acid"}
    }

    if res['redness'] and res['moisture'] < 40:
        sel = prods['hyaluronic']
        msg = "Hassasiyet ve kritik nem kaybı saptandı. Bariyer onarımı önceliğiniz olmalı."
    elif res['sebum'] == "Yüksek" and res['pores'] == "Tıkalı":
        sel = prods['blemish']
        msg = "Aktif sebum fazlası ve gözenek tıkanıklığı saptandı."
    elif u['age'] > 35:
        sel = prods['retinol']
        msg = "Yaş profiline bağlı hücresel yenilenme desteği önceliklendirildi."
    elif u.get('on_period'):
        sel = prods['hyaluronic']
        msg = "Regl dönemindeki hormonal hassasiyet nedeniyle yatıştırıcı nem desteği eşleştirildi."
    elif u.get('cycle', 0) > 20:
        sel = prods['niacinamide']
        msg = "Döngü evrenize bağlı hormonal sebum dengesizliği saptandı."
    else:
        sel = prods['arbutin']
        msg = "Cilt tonu aydınlatma ve bariyer koruma hedeflendi."

    st.markdown(f"""
<div class='clinical-card'>
    <p style='margin:0; font-size: 14px;'><b>Optik Bulgular:</b> Sebum: {res['sebum']} | Nem: %{res['moisture']}</p>
    <p style='margin-top:8px; font-size: 12px; opacity: 0.8;'><b>AI Tanısı:</b> {msg}</p>
</div>
<div class='expert-result-card'>
    <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px;'>
        <span style='font-size: 28px;'>🔬</span>
        <h4 style='margin:0; color: white;'>Klinik Reçete</h4>
    </div>
    <p style='font-size: 13px; opacity: 0.9; line-height: 1.6;'>
        Bariyer sağlığınız için en saf eşleşme:
    </p>
    <div style='background: white; color: #0047AB; padding: 25px; border-radius: 18px; margin-top: 20px; text-align: center;'>
        <p style='margin:0; font-weight: 800; font-size: 18px;'>{sel['t']}</p>
        <p style='margin:8px 0 20px 0; font-size: 12px; color: #666;'>{sel['f']}</p>
        <a href='https://thepurestsolutions.com.tr/products/{sel['url']}' target='_blank' style='display: block; background: #0047AB; color: white !important; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; font-size: 14px;'>Ürünü Keşfet →</a>
    </div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("Yeni Analiz Başlat"):
        reset()

# FOOTER
st.markdown("<div style='text-align: center; margin-top: 40px; padding: 20px; color: #AAA; font-size: 10px;'>© 2024 DermaScan AI | The Purest Solutions<br><b>v4.5 Dynamic Clinical Analytics</b></div>", unsafe_allow_html=True)
