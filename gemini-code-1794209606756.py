import time
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(page_title="Simulasi Gempa", page_icon="🏗️", layout="wide")


def draw_building(amplitude, floors, time_seconds=0):
    """Create one frame of the illustrative building-sway simulation."""
    fig, ax = plt.subplots(figsize=(6, 6), layout="tight")
    y = np.linspace(0, floors * 3, floors + 1)
    x = amplitude * (y / y[-1]) ** 2

    ax.axhline(0, color="black", linewidth=3)
    ax.plot(x - 1.5, y, "r-o", x + 1.5, y, "r-o", linewidth=3)
    for floor_y, offset in zip(y, x):
        ax.plot([offset - 1.5, offset + 1.5], [floor_y, floor_y], "gray", "--", alpha=0.6)

    limit = max(15, abs(amplitude) + 5)
    ax.set(
        xlim=(-limit, limit),
        ylim=(-1, floors * 3 + 5),
        title=f"Goyangan (waktu: {time_seconds:.2f} s)",
        xlabel="Simpangan / Goyangan (m)",
    )
    return fig


def page_earthquake():
    st.header("🏗️ Simulasi Gedung Tahan Gempa")
    st.write(
        "Uji goyangan gedung saat gempa untuk mengamati simulasi sederhana "
        "dengan beberapa jenis struktur bangunan."
    )
    st.warning(
        "Simulasi ini hanya ilustrasi edukatif, bukan model teknik atau alat "
        "untuk menilai keamanan bangunan nyata."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        floors = st.slider("Jumlah Lantai", 1, 3, 5)
        material = st.selectbox(
            "Material", ["Beton Biasa", "Beton Bertulang", "Baja & Peredam"]
        )
        magnitude = st.slider("Magnitudo", 1.0, 10.0, 6.0, 0.5)
        st.info("💡 Beton Biasa: Rapuh | Beton Bertulang: Tahan tarik | Peredam: Serap getaran")

    # Parameter redaman dan skala respons untuk model sederhana ini.
    material_params = {
        "Beton Biasa": (0.02, 15.0),
        "Beton Bertulang": (0.07, 10.0),
        "Baja & Peredam": (0.25, 5.0),
    }
    damping, stiffness_scale = material_params[material]

    with col2:
        plot_placeholder = st.empty()
        status_placeholder = st.empty()
        progress_placeholder = st.empty()

        initial_fig = draw_building(0, floors)
        try:
            plot_placeholder.pyplot(initial_fig, clear_figure=True)
        finally:
            plt.close(initial_fig)

        status_placeholder.info("Klik tombol untuk memulai simulasi.")

        if st.button("🚀 MULAI SIMULASI", use_container_width=True, type="primary"):
            times = np.linspace(0, 8, 40)
            progress = progress_placeholder.progress(0.0, text="Menjalankan simulasi...")
            collapsed = False

            for frame, time_seconds in enumerate(times, start=1):
                # Gelombang sinus dengan redaman eksponensial; model ini hanya ilustratif.
                amplitude = (
                    magnitude
                    * (stiffness_scale / 10)
                    * np.exp(-damping * time_seconds)
                    * np.sin(np.pi * time_seconds)
                )

                fig = draw_building(amplitude, floors, time_seconds)
                try:
                    plot_placeholder.pyplot(fig, clear_figure=True)
                finally:
                    plt.close(fig)

                displacement = abs(amplitude)
                if displacement > 6 and material == "Beton Biasa":
                    status_placeholder.error(
                        f"🚨 BAHAYA: Simpangan {displacement:.2f} m "
                        f"pada t={time_seconds:.2f} s."
                    )
                    collapsed = True
                elif displacement > 4:
                    status_placeholder.warning(
                        f"⚠️ SIMPANGAN TINGGI: {displacement:.2f} m "
                        f"pada t={time_seconds:.2f} s."
                    )
                else:
                    status_placeholder.success(
                        f"✅ Simpangan saat ini: {displacement:.2f} m"
                    )

                progress.progress(frame / len(times), text="Menjalankan simulasi...")
                if collapsed:
                    break
                time.sleep(0.04)

            if not collapsed:
                status_placeholder.success("🏁 Simulasi selesai. Pilih parameter lain untuk skenario berbeda.")
                progress.progress(1.0, text="Simulasi selesai.")
            else:
                progress_placeholder.empty()


page_earthquake()
