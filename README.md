# ComfyUI XAV JSON Nodes

Convenient nodes for working with JSON directly inside ComfyUI. Load files, navigate nested structures, create empty containers, modify values, and save the result back — all within your workflow.

## Features

- **XAV Load JSON File** – load and cache JSON from a file.
- **XAV Navigate JSON** – access array elements (by index) or object properties (by string key).
- **XAV JSON to Primitives** – convert the current node to simple types (`int`, `float`, `bool`, `string`).
- **XAV Create Empty JSON Object** – create an empty `{}` or `[]`.
- **XAV Set JSON Value** – set a string value by key in an existing object/array.
- **XAV Set JSON Value From Ref** – insert another JSON node by key.
- **XAV Save JSON to File** – save any node to a file.

All nodes are located in the `XAV/json` category.

## ⚡ Performance & Optimization

These nodes were designed with speed and efficiency in mind:

- **In‑memory caching** – JSON files are loaded only once and stored globally. Subsequent runs reuse the parsed object instantly.
- **Reference‑based access** – navigation and modification work directly on the original Python objects. No deep copies, no serialization/deserialization overhead during edits.
- **Minimal dependencies** – the entire extension uses only Python's built‑in modules; there is zero external library overhead.
- **Fast path for primitives** – conversion to `int`, `float`, `bool`, or `string` uses direct type casting with minimal branching.
- **Lazy evaluation** – objects are not touched until a node actually reads or writes them.

In practice, operations like loading a 10 MB JSON, navigating deep paths, and modifying values happen in microseconds — ideal for high‑throughput ComfyUI workflows.

## Installation

**Zero dependencies !** – uses only Python's standard library; no pip install needed.

### Method 1: via ComfyUI Manager (recommended)

1. Open ComfyUI and go to **Manager** → **Install Custom Nodes**.
2. Search for **ComfyUI XAV JSON Nodes** and click **Install**.
3. Restart ComfyUI.

### Method 2: manual install

Clone the repository into your `custom_nodes` folder:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/your-username/ComfyUI-XAVJsonNodes