import streamlit as st, numpy as np, matplotlib.pyplot as plt, time

st.set_page_config("Simulasi Gempa", "🏗️", layout="wide")

def page_earthquake():
    st.header("🏗️ Simulasi Gedung Tahan Gempa")
    st.write("Uji goyangan gedung saat gempa untuk mengamati ketahanan berbagai jenis struktur bangunan.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        tinggi = st.slider("Jumlah Lantai", 3, 20, 10)
        mat = st.selectbox("Material", ["Beton Biasa", "Beton Bertulang", "Baja & Peredam"])
        mag = st.slider("Magnitudo", 1.0, 10.0, 6.0, 0.5)
        st.info("💡 Beton Biasa: Rapuh | Beton Bertulang: Tahan Tarik | Peredam: Serap Getaran")

    # Set damping & kekakuan berdasarkan material
    params = {"Beton Biasa": (0.02, 15.0), "Beton Bertulang": (0.07, 10.0), "Baja & Peredam": (0.25, 5.0)}
    damp, k = params[mat]

    with col2:
        plot_ph, stat_ph = st.empty(), st.info("Klik tombol untuk memulai simulasi.")

        def draw(amp, t=0):
            fig, ax = plt.subplots(figsize=(6, 6), layout="tight")
            ax.axhline(0, color="k", lw=3)
            y = np.linspace(0, tinggi * 3, tinggi + 1)
            x = amp * (y / y[-1])**2

            # Plot tiang (kiri & kanan) sekaligus
            ax.plot(x - 1.5, y, 'r-o', x + 1.5, y, 'r-o', lw=4)
            # Plot lantai
            for yi, xi in zip(y, x): 
                ax.plot([xi-1.5, xi+1.5], [yi, yi], 'gray', '--', alpha=0.5) 

            batas = max(15, abs(amp) + 5)
            ax.set(xlim=(-batas, batas), ylim=(-1, tinggi*3 + 5), 
                   title=f"Goyangan (Waktu: {t:.2f}s)", xlabel="Simpangan (m)", ylabel="Tinggi (m)")
            return fig

        plot_ph.pyplot(draw(0), clear_figure=True)

        if st.button("🚀 MULAI SIMULASI", use_container_width=True, type="primary"):
            for t in np.linspace(0, 8, 40):
                # Gelombang sinus dengan redaman eksponensial
                amp = mag * (k / 10) * np.exp(-damp * t) * np.sin(np.pi * t)
                plot_ph.pyplot(draw(amp, t), clear_figure=True)

                if abs(amp) > 6 and mat == "Beton Biasa":
                    stat_ph.error(f"🚨 BAHAYA: Simpangan {abs(amp):.2f}m di t={t:.2f}s! Gedung Runtuh.")
                    break
                elif abs(amp) > 4:
                    stat_ph.warning(f"⚠️ KERUSAKAN STRUKTUR: Simpangan {abs(amp):.2f}m di t={t:.2f}s")
                else:
                    stat_ph.success(f"✅ AMAN: Simpangan {abs(amp):.2f}m")
                
                time.sleep(0.04)
            else:
                # Dieksekusi jika loop selesai tanpa 'break'
                stat_ph.success("🏁 Simulasi selesai. Pilih parameter lain untuk skenario berbeda.")

page_earthquake()