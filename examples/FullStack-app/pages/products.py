from dars.all import *
from backend.models import get_db
# ── Server actions ───────────────────────────────────────────────────────
@server_action(csrf_protected=False)
async def get_product_stats():
    """Return aggregate stats for products."""
    try:
        db = get_db()
        row = db.fetch_one("SELECT COUNT(*) as total, AVG(price) as avg_price FROM products")
        if row:
            return {"total": row["total"], "avg_price": round(row["avg_price"] or 0, 2)}
    except Exception:
        pass
    return {"total": 0, "avg_price": 0}

@server_action(csrf_protected=False)
def generate_random_product(name: str, max_price: float = 100.0):
    """Generate a random product preview (does not save to DB)."""
    import random, datetime
    return {
        "name": name,
        "price": round(random.uniform(5.0, max_price), 2),
        "description": f"Randomly generated product at {datetime.datetime.now().isoformat()}",
        "category": random.choice(["electronics", "clothing", "food", "books"]),
    }
@route("/products", route_type=RouteType.PRIVATE, requires_auth=True)
def products():
    # ══════════════════════════════════════════════════════════════════
    # VRefs
    # ═══════════════════════════════════════`═══════════════════════════
    loading_sel   = ".products-loading"
    error_sel     = ".products-error"
    products_sel  = ".products-data"

    is_loading = setVRef(True,  loading_sel)
    has_error  = setVRef(False, error_sel)
    _products  = setVRef([],    products_sel)

    # ══════════════════════════════════════════════════════════════════
    # Fetch products (GET /api/models/products)
    # ══════════════════════════════════════════════════════════════════
    on_fetch_success = runSequence(
        updateVRef(loading_sel, False),
        updateVRef(error_sel,   False),
        updateVRefFromResponse(products_sel),
    )
    on_fetch_error = runSequence(
        updateVRef(loading_sel, False),
        updateVRef(error_sel,   True),
    )
    fetch_trigger, *_ = useFetch(
        "/api/models/products",
        method="GET",
        on_success=on_fetch_success,
        on_error=on_fetch_error,
    )

    # ══════════════════════════════════════════════════════════════════
    # Add Product (POST /api/models/products)
    # ══════════════════════════════════════════════════════════════════
    add_form = collect_form(
        name=V("#prod-name"),
        price=V("#prod-price"),
        description=V("#prod-desc"),
        category=V("#prod-cat"),
    )
    add_validator = FormValidator({
        "name":  [required(), min_length(2), max_length(100)],
        "price": [required()],
    })
    after_add = runSequence(
        clearInput("prod-name"),
        clearInput("prod-price"),
        clearInput("prod-desc"),
        setText("add-result", "Product added! Refreshing list..."),
        fetch_trigger,
    )
    add_action = add_validator.validated_submit(
        url="/api/models/products",
        form_data=add_form,
        on_success=after_add,
        on_error=setText("add-result", "Error adding product"),
    )

    # ══════════════════════════════════════════════════════════════════
    # Generate random product (POST /api/actions/generate_random_product)
    # ══════════════════════════════════════════════════════════════════
    gen_form = collect_form(
        name=V("#gen-name"),
        max_price=V("#gen-max-price"),
    )
    gen_validator = FormValidator({
        "name": [required(), min_length(2)],
    })

    gen_has_data = setVRef(False, ".gen-preview")

    on_gen_success = runSequence(
        updateVRefFromResponse(".gen-preview-name",  key="response.name"),
        updateVRefFromResponse(".gen-preview-price", key="response.price"),
        updateVRefFromResponse(".gen-preview-desc",  key="response.description"),
        updateVRefFromResponse(".gen-preview-cat",   key="response.category"),
        updateVRef(".gen-preview", True),
    )
    on_gen_error = setText("gen-error", "Error generating product")

    generate_action = gen_validator.validated_submit(
        url="/api/actions/generate_random_product",
        form_data=gen_form,
        on_success=on_gen_success,
        on_error=on_gen_error,
    )

    # ══════════════════════════════════════════════════════════════════
    # Stats (POST /api/actions/get_product_stats)
    # ══════════════════════════════════════════════════════════════════
    stats_sel = ".products-stats"
    _stats    = setVRef({}, stats_sel)

    on_stats_success = runSequence(
        updateVRef(stats_sel, False),
        updateVRefFromResponse(".stats-total", key="response.total"),
        updateVRefFromResponse(".stats-avg",   key="response.avg_price"),
    )
    on_stats_error = runSequence(
        updateVRef(stats_sel, False),
        setText(".stats-total", "?"),
        setText(".stats-avg",   "?"),
    )
    stats_trigger, _, _, _ = useFetch(
        "/api/actions/get_product_stats",
        method="POST",
        on_success=on_stats_success,
        on_error=on_stats_error,
    )

    # ══════════════════════════════════════════════════════════════════
    # Product item template (used by Each)
    # ══════════════════════════════════════════════════════════════════
    def product_item(p):
        pname = p.get("name", "__item_name__")         if isinstance(p, dict) else "__item_name__"
        price = p.get("price", "__item_price__")       if isinstance(p, dict) else "__item_price__"
        cat   = p.get("category", "__item_category__") if isinstance(p, dict) else "__item_category__"
        pid   = p.get("id", "__item_id__")             if isinstance(p, dict) else "__item_id__"
        return Container(
            Container(
                Text(f"#{pid}",      style="text-xs text-gray-400"),
                Text(pname,          style="font-semibold text-base"),
                Text(f"${price}",    style="text-green-600 font-bold text-lg"),
                style="flex items-center justify-between gap-2",
            ),
            Text(cat, style="text-xs text-gray-500 uppercase"),
            style="p-3 border rounded-lg bg-white shadow-sm",
        )

    # In your page:
    
    # ══════════════════════════════════════════════════════════════════
    # Page layout
    # ══════════════════════════════════════════════════════════════════
    page = Page(
        Container(
            Head("Product Manager - Dars Data Layer Demo"),
            # ── Header ──────────────────────────────────────────────
            Container(
                Text("Product Manager",
                     style="text-3xl font-bold text-gray-800"),
                Text("DarsModel · Database · Middleware · Server Actions · Auto CRUD",
                     style="text-xs text-gray-500"),
                style="text-center mb-6",
            ),

            # ── Loading ─────────────────────────────────────────────
            Show(
                is_loading,
                Container(
                    Spinner(),
                    Text("Loading products…", style="text-gray-500 ml-2"),
                    style="flex items-center justify-center gap-2 mb-4",
                ),
            ),

            # ── Error ───────────────────────────────────────────────
            Show(
                has_error,
                Container(
                    Text("Could not load products. Is the backend running?",
                         style="text-red-600"),
                    style="bg-red-50 border border-red-200 rounded-lg p-3 mb-4",
                ),
            ),

            # ── Product Catalog ─────────────────────────────────────
            Container(
                Text("Product Catalog",
                     style="text-lg font-semibold mb-3 text-gray-700"),
                Each(
                    items=_products,
                    render=product_item,
                    class_name="space-y-2 mb-6 min-h-[60px]",
                ),
                style="mb-6",
            ),

            # ── Add Product ─────────────────────────────────────────
            Container(
                Text("Add Product",
                     style="text-base font-semibold mb-3 text-gray-700"),

                Input(id="prod-name", placeholder="Product name",
                      style="border rounded px-3 py-2 w-full mb-1"),
                Text("", id="prod-name-error",
                     style="text-red-500 text-sm mb-1"),

                Input(id="prod-price", placeholder="Price (e.g. 29.99)",
                      style="border rounded px-3 py-2 w-full mb-1"),
                Text("", id="prod-price-error",
                     style="text-red-500 text-sm mb-1"),

                Input(id="prod-desc", placeholder="Description (optional)",
                      style="border rounded px-3 py-2 w-full mb-1"),

                Select(id="prod-cat", options=[
                    SelectOption("electronics", "Electronics"),
                    SelectOption("clothing",   "Clothing"),
                    SelectOption("food",       "Food"),
                    SelectOption("books",      "Books"),
                ], style="border rounded px-3 py-2 w-full mb-3"),

                Text("", id="add-result",
                     style="text-green-600 text-sm mb-2"),

                Container(
                    Button("Add Product",
                           on_click=add_action,
                           style="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"),
                    Button("↻ Refresh",
                           on_click=fetch_trigger,
                           style="bg-transparent text-blue-600 px-4 py-2 border border-blue-600 rounded"),
                    style="flex gap-2",
                ),
                style="bg-white border rounded-xl p-4 mb-6 shadow-sm",
            ),

            # ── Generate Random Product ──────────────────────────────
            Container(
                Container(
                    Text("Generate Random Product",
                         style="text-base font-semibold text-gray-700"),
                    Text("Create a random product via @server_action",
                         style="text-xs text-gray-500"),
                    style="mb-3",
                ),

                Input(id="gen-name", placeholder="Product name (e.g. Gadget)",
                      style="border rounded px-3 py-2 w-full mb-1"),
                Text("", id="gen-name-error",
                     style="text-red-500 text-sm mb-1"),

                Input(id="gen-max-price", placeholder="Max price (e.g. 200)",
                      style="border rounded px-3 py-2 w-full mb-3"),

                Text("", id="gen-error",
                     style="text-red-500 text-sm mb-2"),

                # Preview card — hidden until a product is generated
                Show(
                    gen_has_data,
                    Container(
                        Text("Preview",
                             style="text-sm font-semibold text-purple-700 mb-2"),

                        Container(
                            Text("Name:",    style="text-xs text-gray-500 w-20"),
                            Text("", class_name="gen-preview-name",
                                 style="text-sm font-medium text-gray-900"),
                            style="flex gap-2 mb-1",
                        ),
                        Container(
                            Text("Price:",   style="text-xs text-gray-500 w-20"),
                            Text("", class_name="gen-preview-price",
                                 style="text-sm font-medium text-green-600"),
                            style="flex gap-2 mb-1",
                        ),
                        Container(
                            Text("Category:", style="text-xs text-gray-500 w-20"),
                            Text("", class_name="gen-preview-cat",
                                 style="text-sm text-gray-700"),
                            style="flex gap-2 mb-1",
                        ),
                        Container(
                            Text("Description:", style="text-xs text-gray-500 w-20"),
                            Text("", class_name="gen-preview-desc",
                                 style="text-xs text-gray-500"),
                            style="flex gap-2",
                        ),
                        style="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-3",
                    ),
                ),

                Button("Generate Random",
                       on_click=generate_action,
                       style="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"),
                style="bg-purple-50/50 border border-purple-200 rounded-xl p-4 mb-6",
            ),

            # ── Stats ────────────────────────────────────────────────
            Container(
                Container(
                    Text("Server Action Stats",
                         style="text-base font-semibold text-gray-700"),
                    style="mb-2",
                ),

                Show(
                    _stats,
                    Container(
                        Container(
                            Text("Total products:", style="font-medium"),
                            Text("", class_name="stats-total",
                                 style="font-bold ml-1"),
                            style="flex gap-1 mb-1",
                        ),
                        Container(
                            Text("Average price: $", style="font-medium"),
                            Text("", class_name="stats-avg",
                                 style="font-bold text-green-600 ml-1"),
                            style="flex gap-1 mb-2",
                        ),
                    ),
                ),

                Button("Refresh Stats",
                       on_click=stats_trigger,
                       style="bg-cyan-600 text-white px-3 py-1.5 rounded text-sm hover:bg-cyan-700"),
                style="bg-cyan-50 border border-cyan-200 rounded-xl p-4",
            ),

            style="max-w-2xl mx-auto p-8 font-sans",
        ),
    )

    page.add_script(fetch_trigger)
    page.add_script(stats_trigger)

    return page
