from dars.all import App, Page, GridLayout, FlexLayout, Button, Text, Image

app = App(title="Multipage Layout Demo")

# Página 1: Grid responsive
page1_grid = GridLayout(rows=2, cols=2, gap="2vw")
page1_grid.add_child(Text("Grid Top Left"), row=0, col=0, anchor="top-left")
page1_grid.add_child(Button("Grid Center"), row=0, col=1, anchor="center")
page1_grid.add_child(Image(src="https://placehold.co/120x120", alt="Demo", style={"width": "100%"}), row=1, col=0, col_span=2, anchor="bottom")
page1 = Page(page1_grid)

# Página 2: Flex responsive
page2_flex = FlexLayout(direction="row", wrap="wrap", gap="2vw", justify="center", align="center")
page2_flex.add_child(Text("Flex Start"), anchor="left")
page2_flex.add_child(Button("Flex Center"), anchor="center")
page2_flex.add_child(Image(src="https://placehold.co/120x120", alt="Demo", style={"width": "100%"}), anchor="right")
page2 = Page(page2_flex)

app.add_page("grid", page1, title="Grid Page", index=True)
app.add_page("flex", page2, title="Flex Page")

if __name__ == "__main__":
    app.rTimeCompile()
