import sys
import os

def main():
    # Determine the directory where the exe (or script) lives
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
        # CRITICAL FIX: When frozen, streamlit.config.__file__ won't contain
        # "site-packages", so developmentMode defaults to True which crashes
        # when server.port is explicitly set. We monkey-patch this BEFORE
        # streamlit config is parsed.
        import streamlit.config as _cfg
        _cfg._global_development_mode = lambda: False
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    script_path = os.path.join(base_dir, "MuonDetector.py")

    # Set environment variables as fallback
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '127.0.0.1'

    # Hijack sys.argv so Streamlit thinks it was launched normally
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--server.headless=true",
        "--server.port=8501",
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false",
    ]

    from streamlit.web.cli import main as st_main
    st_main()

if __name__ == "__main__":
    main()
