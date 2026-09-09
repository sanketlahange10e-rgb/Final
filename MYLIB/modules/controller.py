import os
import threading
import multiprocessing
from MYLIB.modules.Login_controller import login_controller


# ── Must be at MODULE LEVEL (not nested) so multiprocessing can pickle it ──
def _calculate_routes_worker():
    """
    Runs in a completely separate OS process.
    Has its own GIL — cannot freeze tkinter no matter how CPU-heavy it is.
    """
    from MYLIB.modules.bus_routing import calculate_routes
    calculate_routes()


def controller():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    refresh_in_progress = threading.Event()

    def Refresh(on_complete=None):
        if refresh_in_progress.is_set():
            print("Refresh already in progress. Skipping duplicate call.")
            return
        refresh_in_progress.set()

        def watcher():
            try:
                p = multiprocessing.Process(
                    target=_calculate_routes_worker,
                    daemon=True
                )
                p.start()
                p.join()          # watcher thread blocks here — NOT the main thread
                print("Refresh process finished.")
                if on_complete:
                    on_complete()  # caller must use root.after() for any UI work
            finally:
                refresh_in_progress.clear()

        t = threading.Thread(target=watcher, daemon=True)
        t.start()
        # Returns immediately to the caller

    # Always run Refresh once before any other logic
    Refresh()

    # Only compute on startup if no route data exists yet.
    # If bus_routes.csv already exists, skip startup compute — show old data instantly.
    route_csv = os.path.join(base_dir, 'bus_routes.csv')
    if not os.path.exists(route_csv):
        print("No route data found — computing in background...")
        # Refresh()  # Already called above

    # login_controller MUST run on the main thread (tkinter requirement).
    # Do NOT wrap this in threading.Thread.
    login_controller(refresh=Refresh)