# This code example demonstrates how to convert PNG to SVG
import aspose.words as aw

#  Create document object
doc = aw.Document()

# Create a document builder object
builder = aw.DocumentBuilder(doc)

# Load and insert PNG image
shape = builder.insert_image("test.png")

# Specify image save format as SVG
saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)

# Save image as SVG
shape.get_shape_renderer().save("test.svg", saveOptions)
