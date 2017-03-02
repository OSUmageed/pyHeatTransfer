from kivy.app import App
import kivy.uix.scatter as kS
import kivy.uix.label as kL
import kivy.uix.floatlayout as kF

class TutorialApp(App):
    def build(self):
        fL = kF.FloatLayout()
        sC = kS.Scatter()
        lbl = kL.Label(text='Hello There Nora', font_size=150)

        fL.add_widget(sC)
        sC.add_widget(lbl)
        return fL

if __name__ == "__main__":
    TutorialApp().run()