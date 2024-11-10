import requests

from sweepai.config.server import LICENSE_KEY, NO_LICENSE
from sweepai.utils.cache import create_cache

cache = create_cache()


@cache.memoize(expire=60 * 5)  # 5 minute cache for failed requests
def fetch_license_data(license_key: str) -> requests.Response:
    return requests.post(
        "https://api.keygen.sh/v1/accounts/sweep-dev/licenses/actions/validate-key",
        headers={
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        },
        json={"meta": {"key": license_key}},
    )


@cache.memoize(expire=60 * 60 * 24)  # 1 day cache for successful requests
def validate_license():
    # Validate the license key
    if NO_LICENSE:
        return True
    if LICENSE_KEY is None:
        raise ValueError(
            "No license key provided, please set the LICENSE_KEY environment variable or get a license key from https://deploy.sweep.dev."
        )
    response = fetch_license_data(LICENSE_KEY)
    if response.status_code != 200:
        raise ValueError(
            "License key is invalid or expired. Please contact us at team@sweep.dev to upgrade to an enterprise license."
        )
    obj = response.json()
    if obj["data"]["attributes"]["status"] not in ("ACTIVE", "EXPIRING"):
        raise ValueError(
            "License key is not active. Please contact us at team@sweep.dev to upgrade to an enterprise license."
        )
    return True


if __name__ == "__main__":
    assert validate_license()
