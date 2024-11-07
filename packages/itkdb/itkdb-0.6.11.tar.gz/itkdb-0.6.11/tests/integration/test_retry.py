from __future__ import annotations

import logging

import betamax
import pytest

import itkdb


def test_get_attachment_retry(auth_client, tmpdir, caplog):
    """
    Call getComponentAttachment and check it redirects to old API
    """
    with betamax.Betamax(auth_client).use_cassette("test_retry.test_get_image_retry"):
        with caplog.at_level(logging.WARNING, "itkdb.client"):
            # Test that calling new method retries with the old one
            image = auth_client.get(
                "getComponentAttachment",
                json={
                    "code": "bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9",
                    "component": "abcdef0123456789abcdef0123456789",
                },
            )
            assert "retrying as 'uu-app-binarystore/getBinaryData'" in caplog.text
        assert isinstance(image, itkdb.models.ImageFile)
        assert image.suggested_filename == "PB6.CR2"
        assert image.extension == "cr2"
        temp = tmpdir.join("saved_image_new.cr2")
        nbytes = image.save(filename=temp.strpath)
        assert nbytes == 1166


def test_get_attachment_retry_doesnt_loop(auth_client):
    """
    Check for exception if the old API fails too
    """
    with betamax.Betamax(auth_client).use_cassette("test_retry.test_get_image_none"):
        with pytest.raises(itkdb.exceptions.ResponseException) as exc:
            # Test that calling with bad data doesn't loop
            auth_client.get(
                "getComponentAttachment",
                json={
                    "code": "bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9",
                    "component": "abcdef0123456789abcdef0123456789",
                },
            )

        # Retrying keeps the old exception too
        assert exc.value.__cause__ is not None
