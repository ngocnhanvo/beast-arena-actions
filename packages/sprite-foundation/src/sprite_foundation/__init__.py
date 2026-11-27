"""Portable 2D sprite-source integrity checks.

Important: structural checks NEVER establish human visual acceptance.
"""
from .audit import audit_manifest, audit_manifest_file, APPROVAL_ENV
__all__ = ["audit_manifest", "audit_manifest_file", "APPROVAL_ENV"]
__version__ = "0.1.0"