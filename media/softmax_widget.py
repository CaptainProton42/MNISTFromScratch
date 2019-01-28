from ipywidgets import Box, HBox, VBox, FloatSlider, FloatProgress, Label, Layout
s1 = FloatSlider(description='Apple', min=-5, max=5, step=0.01, value=0, layout=Layout(width='90%'))
s2 = FloatSlider(description='Horse', min=-5, max=5, step=0.01, value=0, layout=Layout(width='90%'))
s3 = FloatSlider(description='Flower', min=-5, max=5, step=0.01, value=0, layout=Layout(width='90%'))
s4 = FloatSlider(description='Car', min=-5, max=5, step=0.01, value=0, layout=Layout(width='90%'))
p1 = FloatProgress(min=0, max=1, step=0.01, value=0)
p2 = FloatProgress(min=0, max=1, step=0.01, value=0)
p3 = FloatProgress(min=0, max=1, step=0.01, value=0)
p4 = FloatProgress(min=0, max=1, step=0.01, value=0)
l1 = Label(value="0.00")
l2 = Label(value="0.00")
l3 = Label(value="0.00")
l4 = Label(value="0.00")

import numpy as np
values = np.array([0.0, 0.0, 0.0, 0.0])
def softmax(i):
    return np.exp(values[i]) / np.sum(np.exp(values))
	
def set_values():
    l1.value = "%.2f" % softmax(0)
    l2.value = "%.2f" % softmax(1)
    l3.value = "%.2f" % softmax(2)
    l4.value = "%.2f" % softmax(3)
    p1.value = softmax(0)
    p2.value = softmax(1)
    p3.value = softmax(2)
    p4.value = softmax(3)

def on_value_change(change):
    if change.owner == s1:
        values[0] = change.new
    if change.owner == s2:
        values[1] = change.new
    if change.owner == s3:
        values[2] = change.new
    if change.owner == s4:
        values[3] = change.new
    set_values()

s1.observe(on_value_change, names='value')
s2.observe(on_value_change, names='value')
s3.observe(on_value_change, names='value')
s4.observe(on_value_change, names='value')

def main():
	set_values()
	left_box = VBox([s1, s2, s3, s4], layout=Layout(width='50%'))
	middle_box = VBox([p1, p2, p3, p4])
	right_box = VBox([l1, l2, l3, l4])
	return HBox([left_box, middle_box, right_box])
	
if __name__ == "__main__":
	main()