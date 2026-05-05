[app]

# App title shown on device
title = Snake and Ladders

# Package name (must be unique, use reverse domain)
package.name = snakeladders

# Package domain
package.domain = com.yourusername

# Source code directory (relative to buildozer.spec)
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf

# App version
version = 1.0

# Requirements — kivy and its deps
requirements = python3,kivy==2.3.0,kivymd

# Orientation
orientation = portrait

# Android API targets
android.api = 33
android.minapi = 26
android.ndk = 25b
android.sdk = 33

# Permissions
android.permissions = INTERNET

# Icon (place icon.png in assets/ folder — 512x512 recommended)
# icon.filename = %(source.dir)s/assets/icon.png

# Presplash (launch screen image)
# presplash.filename = %(source.dir)s/assets/presplash.png

# Presplash background color
android.presplash_color = #141210

# Accept Android SDK license
android.accept_sdk_license = True

# Build type: debug or release
android.build_type = apk

# Arch — arm64-v8a covers most modern Android devices
android.archs = arm64-v8a

# Allow backup
android.allow_backup = True

# Fullscreen — hides status bar on Android
fullscreen = 1

[buildozer]

# Buildozer log level: 0=error 1=info 2=debug
log_level = 2

# Warn on root usage
warn_on_root = 1
