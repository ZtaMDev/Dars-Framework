from dars.all import *
from dars.core.state import dState, Mod

app = App(title="Dars State Mods Demo", theme="dark")
# Base components
counter_text = Text("0", id="Counter", style={
    'font-size': '48px',
    'font-weight': 'bold',
    'margin-bottom': '16px'
})
status_text = Text("State: 0", id="Status", style={'margin-bottom': '16px'})

# Define a state bound to the counter_text element
counter = dState("counter", component=counter_text, states=[0,1,2,3])

# cState rules (compact Mod specs)
# - When entering state 1: increment text by +1
counter.cState(1, mods=[
    Mod.inc(counter_text, prop='text', by=1),
    Mod.set(status_text, text='State: 1'),
])
# - When entering state 2: decrement text by -1
counter.cState(2, mods=[
    Mod.dec(counter_text, prop='text', by=1),
    Mod.set(status_text, text='State: 2'),
])
# - When entering state 3: toggle CSS class and append text
counter.cState(3, mods=[
    Mod.toggle_class(counter_text, name='highlight', on=None),
    Mod.append_text(counter_text, value='!'),
    # Prepare status to show state 0 upon auto-cycle (state 0 is immutable, no rules)
    Mod.set(status_text, text='State: 0'),
])
# Auto-cycle back to 0 after applying state 3 mods
counter.cState(3).goto(0)

# Controls
inc_btn = Button("Next (+1)", id="NextBtn", on_click=counter.state(goto='+1'))
dec_btn = Button("Prev (-1)", id="PrevBtn", on_click=counter.state(goto='-1'))
# Full replace example (cComp=True) using deferred mod to avoid mutating at authoring time
swap_btn = Button(
    "Swap HTML",
    id="SwapBtn",
    on_click=counter.state(2, cComp=True, render=counter_text.mod(text="SWAPPED"))
)

# Layout
index = Page(
    Container(
        counter_text,
        status_text,
        Container(
            inc_btn,
            dec_btn,
            swap_btn,
            class_name="controls",
            style={'display': 'flex', 'gap': '8px'}
        ),
        class_name="wrapper",
        style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'padding': '40px'}
    )
)


app.add_page("index", index, title="State Mods Demo", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
