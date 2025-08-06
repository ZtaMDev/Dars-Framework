from dars.all import App, GridLayout, Button, Text, Image, AnchorPoint

app = App(title="GridLayout Responsive Example")

grid = GridLayout(rows=2, cols=2, gap="2vw")
grid.add_child(Text("Top Left"), row=0, col=0, anchor="top-left")
grid.add_child(Button("Center"), row=0, col=1, anchor="center")
grid.add_child(Image(src="https://placehold.co/120x120", alt="Demo", style={"width": "100%"}), row=1, col=0, col_span=2, anchor=AnchorPoint(x="center", y="bottom"))

app.set_root(grid)

if __name__ == "__main__":
    app.rTimeCompile()
