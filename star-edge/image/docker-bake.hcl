group "default" {
    targets = ["autossh", "ffmpeg", "edge"]
}
target "autossh" {
    context = "./autossh"
    dockerfile = "./autossh/Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64",
        "linux/arm/v7"
    ]
    tags = ["itlabstar/autossh:ddl"]
    output = ["type=registry"]
}
target "ffmpeg" {
    context = "./ffmpeg"
    dockerfile = "./ffmpeg/Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64",
        "linux/arm/v7"
    ]
    tags = ["itlabstar/ffmpeg:ddl"]
    output = ["type=registry"]
}
target "edge" {
    context = "./edge"
    dockerfile = "./edge/Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64",
        "linux/arm/v7"
    ]
    tags = ["itlabstar/edge:ddl"]
    output = ["type=registry"]
}