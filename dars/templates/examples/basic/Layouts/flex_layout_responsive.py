from dars.all import *

app = App(title="FlexLayout Responsive Example")

flex = FlexLayout(direction="row", wrap="wrap", gap="2vw", justify="center", align="center")
flex.add_child(Text("Start"), anchor="left")
flex.add_child(Button("Center", on_click=this().state(text="Clicked!", style={'background-color': '#2ecc71'})), anchor="center")
flex.add_child(Image(src="https://placehold.co/120x120", alt="Demo", style={"width": "100%"}), anchor=AnchorPoint(x="right", y="bottom"))

app.set_root(flex)

if __name__ == '__main__':
    app.rTimeCompile()
