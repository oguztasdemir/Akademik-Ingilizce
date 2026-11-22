import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_web_gui_and_dataset_exist():
    assert (ROOT / "Web Gui" / "index.html").exists()
    dataset_dir = ROOT / "Dataset"
    assert dataset_dir.exists()
    json_files = list(dataset_dir.rglob("*.json"))
    assert json_files, "No JSON datasets found"
    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        assert data is not None


def test_api_js_syntax():
    node = shutil.which("node")
    if not node:
        return
    api_dir = ROOT / "api"
    if not api_dir.exists():
        return
    for jf in api_dir.rglob("*.js"):
        proc = subprocess.run([node, "--check", str(jf)], capture_output=True, text=True)
        assert proc.returncode == 0, f"JS syntax error in {jf.name}: {proc.stderr}"
