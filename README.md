# Magie
A Python lib to help program with PyGame.

# Install
```
python -m pip install git+https://github.com/NiumXp/Magie
```

# Quick example
```python
import magie


class Counter(magie.utils.Text):
    def __init__(self):
        font = magie.Font.get_default_font(size=250)
        super().__init__(position=(0, 0), font=font, state=magie.State.ENABLED)

        self.number = 5

        timer = magie.Timer(interval=1, target=self.update, loop=True)
        self.add_timer(timer, enable=True)

    @property
    def text(self):
        return str(self.number)

    def update(self, timer):
        if self.number == 0:
            timer.stop()
        else:
            self.number -= 1


app = magie.Magie(width=1024, height=720)

counter = Counter()
app.extend(counter)

app.build()
```
