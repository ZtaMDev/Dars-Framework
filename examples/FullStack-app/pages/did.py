"""
tasklist.py — Task Manager demo using Dars production-grade features.

Uses:
  - useFetch  (trigger added as page script, runs on load)
  - Each      (runtime list rendering from VRef — no custom DAP ops)
  - Show      (conditional rendering driven by VRef)
  - FormValidator + collect_form  (client-side validation before submit)
  - updateVRef, runSequence, clearInput
"""
from dars.all import *


@route("/tasklist", route_type=RouteType.SSR)
def tasklist():
    # ── VRefs ──────────────────────────────────────────────────────────
    loading_sel = ".tasks-loading"
    error_sel   = ".tasks-error"
    tasks_sel   = ".tasks-data"   # holds the full API response {tasks:[...]}

    is_loading = setVRef(True,  loading_sel)
    has_error  = setVRef(False, error_sel)
    _tasks     = setVRef([],    tasks_sel)

    # ── Fetch callbacks ────────────────────────────────────────────────
    # network_request dispatches on_success with ctx = { response: <data> }
    # updateVRefFromResponse stores ctx.response into tasks_sel so Each re-renders.
    on_fetch_success = runSequence(
        updateVRef(loading_sel, False),
        updateVRef(error_sel,   False),
        updateVRefFromResponse(tasks_sel),
    )

    on_fetch_error = runSequence(
        updateVRef(loading_sel, False),
        updateVRef(error_sel,   True),
    )

    # ── useFetch ───────────────────────────────────────────────────────
    fetch_trigger, _lv, _dv, _ev = useFetch(
        "/api/tasks",
        method="GET",
        on_success=on_fetch_success,
        on_error=on_fetch_error,
    )

    # ── Form ───────────────────────────────────────────────────────────
    # Input id = "task-title" so the validator selector "#task-title" matches it.
    task_form = collect_form(title=V("#task-title"))

    validator = FormValidator({
        "title": [required(), min_length(3), max_length(100)],
    })

    after_submit = runSequence(
        clearInput("task-title"),
        fetch_trigger,
    )

    submit_action = validator.validated_submit(
        url="/api/tasks",
        form_data=task_form,
        on_success=after_submit,
        on_error=setText("submit-error", "Error submitting. Try again."),
    )

    submit_action_del = validator.validated_submit(
        url="/api/deltasks",
        form_data=task_form,
        on_success=after_submit,
        on_error=setText("submit-error", "Error submitting. Try again."),
    )

    # ── Task item render template ──────────────────────────────────────
    # Called at export time with _TEMPLATE_SENTINEL (done=False, title="__item_title__", etc.)
    # The resulting HTML is stored in data-each-template.
    # At runtime dom_each_render substitutes __item_<field>__ with real values.
    # We embed "__item_done_class__" as a placeholder in the class so the runtime
    # can inject "line-through text-gray-400" for done tasks.
    def task_item(t):
        raw_title = t.get("title", "__item_title__") if isinstance(t, dict) else "__item_title__"
        title = raw_title if raw_title else "__item_title__"
        item_id = t.get("id", "__item_id__") if isinstance(t, dict) else "__item_id__"
        # Embed a placeholder class that the runtime replaces with the done style
        done_class = "__item_done_class__"
        return Container(
            Text(title, style=f"flex: 1 1 0%", class_name=done_class),
            Text(f"#{item_id}", style="text-xs text-gray-400 ml-2"),
            style="flex items-center gap-2 p-2 border rounded mb-1 bg-white shadow-sm",
        )

    # ── Page ───────────────────────────────────────────────────────────
    page = Page(
        Container(
            Head("Task Manager Demo"),
            Text("Task Manager",
                 style="text-3xl font-bold mb-1 text-indigo-600"),
            Text("useFetch · Each · FormValidator · Show",
                 style="text-xs text-gray-400 mb-6"),

            # Loading indicator
            Show(
                is_loading,
                Container(
                    Spinner(),
                    Text("Loading tasks…", style="text-gray-500 ml-2"),
                    style="flex items-center gap-2 mb-4",
                ),
            ),

            # Error banner
            Show(
                has_error,
                Container(
                    Text("Could not load tasks. Is the backend running?",
                         style="text-red-600"),
                    style="bg-red-50 border border-red-200 rounded p-3 mb-4",
                ),
            ),

            # Task list — rendered at runtime from tasks_vref via Each
            Each(
                items=_tasks,
                render=task_item,
                class_name="space-y-1 mb-6 min-h-[40px]",
            ),

            # Add task form
            Container(
                Text("Add a task", style="font-semibold mb-2"),
                Input(
                    id="task-title",
                    placeholder="Task title (min 3 chars)…",
                    class_name="border rounded px-3 py-2 w-full mb-1",
                ),
                Text("", id="title-error",  style="text-red-500 text-sm mb-1"),
                Text("", id="submit-error", style="text-red-500 text-sm mb-2"),
                Button(
                    "Add Task",
                    on_click=submit_action,
                    style="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700",
                ),
                Button(
                    "Remove Task",
                    on_click=submit_action_del,
                    style="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700",
                ),
                style="bg-white border rounded-xl p-4 shadow-sm mb-4",
            ),

            Button(
                "↻ Refresh",
                on_click=fetch_trigger,
                style="text-sm text-indigo-500 underline bg-transparent border-0",
            ),

            style="max-w-xl mx-auto p-8 font-sans",
        )
    )

    # Trigger fetch on page load
    page.add_script(fetch_trigger)

    return page
