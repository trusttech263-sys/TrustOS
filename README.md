# TrustOS 2.0 — Android starter project

**Developer:** Trust Chakanyuka  
**Brand:** TrustTech  
**Android package ID:** `com.trusttech.trustos`

TrustOS is a Kivy-based Android workspace prototype. It is not a replacement for Android itself.

## Included in this starter

- TrustOS boot screen
- Mobile and desktop-style layouts
- Luxury, Minimal and Cyber themes
- Theme and layout preference storage
- Local notes
- Calculator
- Placeholder launch cards for future TrustFiles, TrustMusic and TrustAI modules

## Run in Pydroid 3 (prototype testing)

1. Install Kivy in Pydroid 3.
2. Open `main.py`.
3. Run it.

## Build a standalone Android APK from your phone

Pydroid 3 runs the Python app, but does not itself provide the full Android SDK/NDK packaging toolchain. This project includes a GitHub Actions workflow to compile the APK in the cloud.

1. Create or sign in to a GitHub account.
2. Create a **new private repository** named `TrustOS`.
3. Upload the contents of this folder, including the hidden `.github` folder and `buildozer.spec`.
4. Open the repository's **Actions** tab.
5. Select **Build TrustOS APK**.
6. Tap **Run workflow** and confirm.
7. Wait for the workflow to finish.
8. Open the successful workflow run, find **Artifacts**, and download `TrustOS-Android-APK`.
9. Extract the downloaded ZIP and install the APK on your Android device. Android may ask you to approve installing apps from the browser or file manager you used.

The first build can take a while because Android build tools and dependencies must be downloaded. Keep the workflow logs if a build fails; they show the error to fix.

## Important notes

- This is a debug APK for testing, not a Play Store release.
- Do not share signing keys or passwords in chat or in the repository.
- Some app cards are placeholders and will be implemented in later releases.
- Build success can depend on upstream Android/Kivy toolchain changes. The workflow is a build setup, not a guarantee that every future build will succeed without maintenance.
