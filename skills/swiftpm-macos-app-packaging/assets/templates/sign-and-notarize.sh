#!/usr/bin/env bash
set -euo pipefail

APP_NAME=${APP_NAME:-MyApp}
APP_IDENTITY=${APP_IDENTITY:-"Developer ID Application: Example (TEAMID)"}
APP_BUNDLE="${APP_NAME}.app"
ROOT=$(cd "$(dirname "$0")/.." && pwd)
if [[ ! -f "$ROOT/version.env" ]]; then
  echo "ERROR: version.env is required; adapt this input to the project's authoritative version source." >&2
  exit 1
fi
unset MARKETING_VERSION BUILD_NUMBER
# shellcheck disable=SC1091
source "$ROOT/version.env"
: "${MARKETING_VERSION:?version.env must declare MARKETING_VERSION}"
: "${BUILD_NUMBER:?version.env must declare BUILD_NUMBER}"
ZIP_NAME="${APP_NAME}-${MARKETING_VERSION}.zip"

ARCHES_VALUE=${ARCHES:-"arm64 x86_64"}
read -r -a ARCH_LIST <<< "$ARCHES_VALUE"
for ARCH in "${ARCH_LIST[@]}"; do
  swift build -c release --arch "$ARCH"
done
ARCHES="${ARCHES_VALUE}" "$ROOT/scripts/package_app.sh" release

ENTITLEMENTS_DIR="$ROOT/.build/entitlements"
APP_ENTITLEMENTS="${APP_ENTITLEMENTS:-${ENTITLEMENTS_DIR}/${APP_NAME}.entitlements}"

codesign --force --timestamp --options runtime --sign "$APP_IDENTITY" \
  --entitlements "$APP_ENTITLEMENTS" \
  "$APP_BUNDLE"

DITTO_BIN=${DITTO_BIN:-/usr/bin/ditto}
umask 077
NOTARY_DIR=$(mktemp -d "${TMPDIR:-/tmp}/app-notarize.XXXXXX")
trap 'rm -rf "$NOTARY_DIR"' EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
NOTARY_ZIP="$NOTARY_DIR/notarize.zip"
"$DITTO_BIN" --norsrc -c -k --keepParent "$APP_BUNDLE" "$NOTARY_ZIP"

if [[ -n "${APP_STORE_CONNECT_API_KEY_P8:-}" && -n "${APP_STORE_CONNECT_KEY_ID:-}" && -n "${APP_STORE_CONNECT_ISSUER_ID:-}" ]]; then
  printf '%s\n' "$APP_STORE_CONNECT_API_KEY_P8" | sed 's/\\n/\n/g' > "$NOTARY_DIR/key.p8"
  xcrun notarytool submit "$NOTARY_ZIP" \
    --key "$NOTARY_DIR/key.p8" \
    --key-id "$APP_STORE_CONNECT_KEY_ID" \
    --issuer "$APP_STORE_CONNECT_ISSUER_ID" \
    --wait
elif [[ -n "${NOTARY_PROFILE:-}" ]]; then
  xcrun notarytool submit "$NOTARY_ZIP" \
    --keychain-profile "$NOTARY_PROFILE" \
    --wait
else
  echo "Missing notarization credentials: set APP_STORE_CONNECT_* env vars or NOTARY_PROFILE." >&2
  exit 1
fi

xcrun stapler staple "$APP_BUNDLE"

xattr -cr "$APP_BUNDLE"
find "$APP_BUNDLE" -name '._*' -delete

"$DITTO_BIN" --norsrc -c -k --keepParent "$APP_BUNDLE" "$ZIP_NAME"

spctl -a -t exec -vv "$APP_BUNDLE"
stapler validate "$APP_BUNDLE"

echo "Done: $ZIP_NAME"
