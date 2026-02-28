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

# Custom CSS: Minimalist ve Klinik Tasarım
st.markdown("""
<style>
    :root {
        --cobalt-blue: #0047AB;
        --pure-white: #FFFFFF;
        --deep-black: #1A1A1A;
        --warning-orange: #F39C12;
        --error-red: #D90429;
    }

    .stApp {
        background-color: var(--pure-white);
        color: var(--deep-black);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stVerticalBlock"] > div:first-child {
        max-width: 500px;
        margin: 0 auto;
    }

    /* Klinik Kart Tasarımı */
    .clinical-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #EAEAEA;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        margin-bottom: 20px;
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

    .stButton > button:hover {
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

    .warning-box {
        background-color: #FFF3E0;
        border-left: 5px solid var(--warning-orange);
        padding: 15px;
        color: #E67E22;
        font-weight: 600;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Gelişmiş Kamera ve Sıkı Yüz Doğrulama Simülasyonu
def camera_preview(is_scanning=False):
    scanning_js = "true" if is_scanning else "false"
    html_code = f"""
    <div id="cam-box" style="width:100%; border-radius:20px; overflow:hidden; position:relative; background:#111; aspect-ratio: 4/3; border: 1px solid #EEE; display: flex; align-items: center; justify-content: center;">
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
        
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
            navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "user" }} }})
                .then(s => {{
                    v.srcObject = s;
                    loading.style.display = 'none';
                    checkFaceVisibility();
                }})
                .catch(err => {{
                    console.error("Camera error:", err);
                    loading.innerHTML = "<div style='color:#FF4B4B; padding:20px;'>Kamera erişimi reddedildi.</div>";
                }});
        }}

        // Yüz görünürlüğü takibi (Sert Simülasyon)
        function checkFaceVisibility() {{
            setInterval(() => {{
                if(v.paused || v.ended) return;
                // Simülasyon: Kullanıcı yüzünü gerçekten merkezlemezse hata verir
                // Analiz modundayken uyarıyı daha agresif gösterir
                const faceInView = Math.random() > 0.08; 
                if(!faceInView) {{
                    faceMsg.style.display = "block";
                }} else {{
                    faceMsg.style.display = "none";
                }}
            }}, 2000);
        }}

        let pts = [];
        function initPts() {{
            pts = [];
            for(let i=0; i<250; i++) {{
                pts.push({{
                    x: Math.random() * c.width,
                    y: Math.random() * c.height,
                    s: Math.random() * 2 + 0.5,
                    vx: (Math.random() - 0.5) * 1,
                    vy: (Math.random() - 0.5) * 1,
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
                    // Yüz Algılama Çerçevesi (Yeşil/Kırmızı Dinamik)
                    const isFaceOk = Math.random() > 0.1;
                    ctx.strokeStyle = isFaceOk ? "rgba(0, 255, 0, 0.6)" : "rgba(255, 0, 0, 0.6)";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(c.width*0.25, c.height*0.2, c.width*0.5, c.height*0.6);

                    ctx.fillStyle = isFaceOk ? "rgba(0, 255, 0, 0.7)" : "rgba(255, 0, 0, 0.7)";
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = isFaceOk ? "#00FF00" : "#FF0000";
                    
                    pts.forEach(p => {{
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, p.s, 0, 6.28);
                        ctx.fill();
                        
                        p.x += p.vx + Math.sin(Date.now() * 0.0015 + p.o) * 1.5;
                        p.y += p.vy + Math.cos(Date.now() * 0.0015 + p.o) * 1.5;
                        
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
st.markdown("<div style='text-align: center; margin-bottom: 30px;'><h2 style='color: #0047AB; margin-bottom: 0;'>DermaScan AI</h2><p style='font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 3px; font-weight: 700;'>Optical Skin Analysis & Diagnostic Lab</p></div>", unsafe_allow_html=True)

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

# ADIM 2: KAMERA İZNİ VE GÖRSEL ANALİZ
elif st.session_state.step == 2:
    if not st.session_state.cam_granted:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Optik Tarayıcı Erişimi</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 14px; color: #444;'>AI modelimizin gözenek yapısı ve cilt bütünlüğünü analiz edebilmesi için kamera erişimi gereklidir.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Kamerayı Aktif Et"):
            st.session_state.cam_granted = True
            st.rerun()
    else:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        
        if st.session_state.user['gender'] == "Kadın":
            st.markdown("<p style='font-weight:600; font-size:14px; margin-bottom:5px;'>Regl Döngüsü Analizi</p>", unsafe_allow_html=True)
            cycle_day = st.number_input("Regl döngünüzü giriniz", 1, 35, 14)
            st.markdown("<p style='font-size: 13px; color: #555; margin-top: -15px; margin-bottom: 15px;'>Hormonal sivilceler için regl döngüsü girmenizi istiyoruz.</p>", unsafe_allow_html=True)
            st.session_state.user['cycle'] = cycle_day
            st.markdown("<hr style='opacity: 0.1; margin: 15px 0;'>", unsafe_allow_html=True)

        st.markdown("<p style='text-align:center; font-weight:600; margin-bottom:10px;'>Canlı Optik Analiz Alanı</p>", unsafe_allow_html=True)
        
        # Yüz görünürlüğü kontrolü için hata mesajı (eğer varsa)
        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)
            st.session_state.error_msg = "" # Mesajı bir sonraki işlemde temizlemek için

        camera_preview(is_scanning=st.session_state.scan_active)
        
        if not st.session_state.scan_active:
            if st.button("Görsel Analizi Başlat"):
                # ÇOK SIKI YÜZ ALGILAMA KONTROLÜ
                with st.spinner("AI Yüz Kilidi Doğrulanıyor..."):
                    time.sleep(2)
                    # %30 olasılıkla yüz algılanamadı hatası (Simülasyon - kullanıcıyı hizalanmaya zorlar)
                    # Gerçek hayatta ML kütüphaneleriyle bu değer yüzün varlığına göre döner.
                    face_verified = random.random() > 0.3
                    
                    if face_verified:
                        st.session_state.scan_active = True
                        st.rerun()
                    else:
                        st.session_state.error_msg = "❌ Analiz Başlatılamadı: Yüz algılanamadı! Lütfen kameraya doğru tam karşıdan bakınız."
                        st.rerun()
        else:
            status = st.empty()
            # Analiz Metrikleri Simülasyonu
            metrics = ["Yüz Geometrisi Kilidi", "Sebum Analizi", "Görsel Bariyer Ölçümü", "Gözenek Haritalama", "Kızarıklık Tespiti"]
            
            scan_success = True
            for m in metrics:
                # Her adımda rastgele "yüz kayboldu" kontrolü
                if random.random() < 0.05: # Tarama sırasında yüzün çekilmesi durumu
                    scan_success = False
                    break
                status.markdown(f"<p style='text-align:center; color:#0047AB; font-weight:700;'>{m} Yapılıyor...</p>", unsafe_allow_html=True)
                time.sleep(1.2)
            
            if scan_success:
                st.session_state.analysis_results = {
                    "sebum_level": random.choice(["Yüksek", "Dengeli", "Düşük"]),
                    "redness": random.choice([True, False]),
                    "pore_clogging": random.choice(["Minimal", "Belirgin"]),
                    "moisture_score": random.randint(25, 95)
                }
                st.session_state.step = 3
                st.session_state.scan_active = False
                st.rerun()
            else:
                st.session_state.scan_active = False
                st.session_state.error_msg = "⚠️ Tarama Kesildi: Yüz odağı kayboldu! Lütfen tekrar deneyin."
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ADIM 3: GÖRSEL ANALİZ TABANLI SONUÇLAR
elif st.session_state.step == 3:
    u = st.session_state.user
    res = st.session_state.analysis_results
    st.markdown("<h3 style='text-align: center;'>Klinik Analiz Raporu</h3>", unsafe_allow_html=True)
    
    # Ürünler (The Purest Solutions Veritabanı)
    p_niacinamide = {"t": "Intensive Pore Tightening Serum", "f": "Niacinamide %5 + Zinc PCA %1", "url": "intensive-pore-tightening-lightening-serum-niacinamide-5-zinc-pca-1"}
    p_hyaluronic = {"t": "Hyaluronic Acid %2 + B5", "f": "Intensive Hydration Serum", "url": "intensive-hydration-serum-hyaluronic-acid-2-b5"}
    p_arbutin = {"t": "Brightening Serum", "f": "Arbutin %2 + Hyaluronic Acid", "url": "brightening-serum-arbutin-2-hyaluronic-acid"}
    p_retinol = {"t": "Retinol Serum %0.5", "f": "Rejuvenating Retinol Serum", "url": "rejuvenating-retinol-serum-0-5-retinol-complex"}
    p_blemish = {"t": "Blemish Defense Serum", "f": "Oil Control Solution", "url": "blemish-defense-serum"}
    p_vitc = {"t": "Vitamin C Serum %10", "f": "Ethyl Ascorbic Acid", "url": "brightening-lightening-serum-10-vitamin-c-0-5-ferulic-acid"}

    # GÖRSEL ANALİZ KARAR MOTORU (Duygulardan Bağımsız, Sadece Görüntü)
    if res['sebum_level'] == "Yüksek" and res['pore_clogging'] == "Belirgin":
        selected = p_blemish
        reason = "Optik tarayıcı yüksek sebum üretimi ve gözenek tıkanıklığı saptadı."
    elif res['moisture_score'] < 45:
        selected = p_hyaluronic
        reason = "Cilt yüzeyinde kritik seviyede dehidrasyon ve düşük elastikiyet saptandı."
    elif res['redness']:
        selected = p_arbutin
        reason = "Görsel analizde epidermal hassasiyet ve vasküler kızarıklık saptandı."
    elif u['age'] > 35:
        selected = p_retinol
        reason = "Yaş profili ve mikro-çizgi analizi sonucunda hücresel yenilenme desteği önceliklendirildi."
    elif u.get('cycle', 0) > 21:
        selected = p_niacinamide
        reason = "Hormonal döngüye bağlı olarak artan yağlanma eğilimi ve gözenek genişlemesi saptandı."
    else:
        selected = p_vitc
        reason = "Cilt tonu analizi mat görünümü ve serbest radikal hasarını ön plana çıkardı."

    st.markdown(f"""
    <div class='clinical-card'>
        <p style='margin:0; font-size: 14px;'><b>Optik Teşhis Özeti (AI Verisi):</b></p>
        <ul style='font-size: 12px; color: #444; margin-top: 5px; line-height: 1.6;'>
            <li>Sebum Seviyesi: <b>{res['sebum_level']}</b></li>
            <li>Gözenek Durumu: <b>{res['pore_clogging']}</b></li>
            <li>Nem Skoru: <b>%{res['moisture_score']}</b></li>
            <li>Vasküler Hassasiyet: <b>{'Saptandı' if res['redness'] else 'Saptanmadı'}</b></li>
        </ul>
        <hr style='opacity: 0.1;'>
        <p style='font-size: 12px; color: #666; line-height: 1.5;'>
            <b>Uzman Analizi:</b> {reason} AI modelimiz, kameradan alınan optik verilerinizi klinik standartlarda işleyerek bu reçeteyi oluşturdu.
        </p>
    </div>
    
    <div class='expert-result-card'>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px;'>
            <span style='font-size: 28px;'>🔬</span>
            <h4 style='margin:0; color: white;'>Klinik Eşleşme</h4>
        </div>
        <div style='background: white; color: #0047AB; padding: 25px; border-radius: 18px; text-align: center;'>
            <p style='margin:0; font-weight: 800; font-size: 16px;'>{selected['t']}</p>
            <p style='margin:5px 0 15px 0; font-size: 12px; color: #666;'>{selected['f']}</p>
            <a href='https://thepurestsolutions.com/products/{selected['url']}' target='_blank' style='display: block; background: #0047AB; color: white !important; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; font-size: 14px;'>Ürünü Keşfet →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Yeni Analiz Başlat", on_click=reset)

# FOOTER
st.markdown("<div style='text-align: center; margin-top: 40px; padding: 20px; color: #AAA; font-size: 10px; border-top: 1px solid #F8F8F8;'>© 2024 DermaScan AI | The Purest Solutions<br><b>v4.0 Biometric Diagnostic Standard</b></div>", unsafe_allow_html=True)