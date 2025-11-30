try:
    from dars.js_lib import DARS_MIN_JS
    print("Successfully imported DARS_MIN_JS")
    print(f"Length: {len(DARS_MIN_JS)}")
except Exception as e:
    print(f"Error importing DARS_MIN_JS: {e}")
    import traceback
    traceback.print_exc()
