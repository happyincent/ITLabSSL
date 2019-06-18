group "default" {
    targets = ["autossh", "ffmpeg", "edge"]
}
target "autossh" {
    context = "./autossh"
    dockerfile = "Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64",
        "linux/arm/v7"
    ]
    tags = ["itlabstar/autossh"]
    output = ["type=registry"]
}
target "ffmpeg" {
    context = "./ffmpeg"
    dockerfile = "Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64",
        "linux/arm/v7"
    ]
    tags = ["itlabstar/ffmpeg"]
    output = ["type=registry"]
}
target "edge" {
    context = "./edge"
    dockerfile = "Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64",
        "linux/arm/v7"
    ]
    tags = ["itlabstar/edge"]
    output = ["type=registry"]
}