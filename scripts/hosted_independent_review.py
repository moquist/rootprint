"""Trusted hosted entrypoint; retain the standalone coordinator's lower default."""

import independent_review as reviewer

if __name__ == "__main__":
    reviewer.MAX_CONTEXT = 1_200_000
    reviewer.main()
