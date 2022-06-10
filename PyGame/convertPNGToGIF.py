from PIL import Image

# program to convert multiple .png files to a single .gif file

if __name__ == "__main__":
    pngFiles = 5
    frames = []
    for i in range(pngFiles):
        file = 'fileName' + str(i) + '.png'
        newFrame = Image.open(file)
        frames.append(newFrame)

    # Save into a GIF file that loops forever
    saveFile = 'saveFileName' + '.gif'
    frames[0].save(saveFile, format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=300, loop=0)
