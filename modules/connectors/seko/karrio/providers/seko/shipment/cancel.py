import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = True  # compute shipment cancel success state

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "PickupOptions",
            # fmt: off
            {
                "shipment_ids": lib.OptionEnum("shipment_ids", lib.to_list),
            },
            # fmt: on
        ),
    )

    # map data to convert karrio model to seko specific type
    request = lib.identity(options.shipment_ids.state or [payload.shipment_identifier])

    return lib.Serializable(request, lib.to_dict)
