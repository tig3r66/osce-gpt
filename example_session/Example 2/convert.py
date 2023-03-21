import ffmpeg

input_file = "streamlit-website-2023-03-21-09-03-24.webm"
output_file = "output.mp4"

# Open the input WebM file
stream = ffmpeg.input(input_file)

# Convert to MP4 format
stream = ffmpeg.output(stream, output_file)

# Run the conversion
ffmpeg.run(stream)
