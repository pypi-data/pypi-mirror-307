import dataclasses
import typing

from oci_client import _client, _helpers


@dataclasses.dataclass  # noqa: PLR0904
class Client(_client.Client):
    def net_monitor_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def net_monitor_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def net_monitor_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def net_monitor_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def net_monitor_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def net_monitor_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def net_monitor_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def net_monitor_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def net_monitor_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='net_monitor',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocb_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocb_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocb_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocb_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocb_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocb_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocb_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocb_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocb_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocb',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def access_governance_cp_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def access_governance_cp_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def access_governance_cp_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def access_governance_cp_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def access_governance_cp_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def access_governance_cp_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def access_governance_cp_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def access_governance_cp_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def access_governance_cp_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='access_governance_cp',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def adm_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='adm',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def adm_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='adm',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def adm_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='adm',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def adm_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='adm',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def adm_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='adm',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def adm_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='adm',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def adm_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='adm',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def adm_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='adm',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def adm_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='adm',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def advisor_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def advisor_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def advisor_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def advisor_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def advisor_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def advisor_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def advisor_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def advisor_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def advisor_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='advisor',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def analytics_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def analytics_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def analytics_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def analytics_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def analytics_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def analytics_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def analytics_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def analytics_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def analytics_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='analytics',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def announcements_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def announcements_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def announcements_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def announcements_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def announcements_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def announcements_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def announcements_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def announcements_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def announcements_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='announcements',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def anomalydetection_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def anomalydetection_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def anomalydetection_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def anomalydetection_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def anomalydetection_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def anomalydetection_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def anomalydetection_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def anomalydetection_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def anomalydetection_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='anomalydetection',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def api_gateway_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def api_gateway_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def api_gateway_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def api_gateway_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def api_gateway_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def api_gateway_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def api_gateway_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def api_gateway_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def api_gateway_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='api_gateway',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_config_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_config_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_config_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_config_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_config_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_config_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_config_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_config_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_config_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_config',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_control_plane_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_control_plane_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_control_plane_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_control_plane_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_control_plane_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_control_plane_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_control_plane_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_control_plane_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_control_plane_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_control_plane',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_synthetic_monitoring_trace(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='apm_synthetic_monitoring',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_trace_explorer_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_trace_explorer_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_trace_explorer_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_trace_explorer_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_trace_explorer_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def apm_trace_explorer_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_trace_explorer_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_trace_explorer_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def apm_trace_explorer_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='apm_trace_explorer',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def audit_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='audit',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def audit_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='audit',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def audit_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='audit',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def audit_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='audit',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def audit_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='audit',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def audit_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='audit',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def audit_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='audit',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def audit_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='audit',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def audit_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='audit',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def autoscaling_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def autoscaling_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def autoscaling_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def autoscaling_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def autoscaling_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def autoscaling_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def autoscaling_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def autoscaling_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def autoscaling_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='autoscaling',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bastion_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bastion_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bastion_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bastion_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bastion_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bastion_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def bastion_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def bastion_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def bastion_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bastion',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bigdata_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bigdata_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bigdata_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bigdata_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bigdata_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def bigdata_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def bigdata_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def bigdata_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def bigdata_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='bigdata',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def blockchain_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def blockchain_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def blockchain_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def blockchain_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def blockchain_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def blockchain_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def blockchain_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def blockchain_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def blockchain_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='blockchain',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def budgets_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def budgets_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def budgets_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def budgets_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def budgets_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def budgets_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def budgets_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def budgets_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def budgets_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='budgets',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificates_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificates_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificates_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificates_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificates_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificates_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def certificates_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def certificates_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def certificates_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificates',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificatesmgmt_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificatesmgmt_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificatesmgmt_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificatesmgmt_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificatesmgmt_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def certificatesmgmt_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def certificatesmgmt_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def certificatesmgmt_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def certificatesmgmt_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='certificatesmgmt',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def cloud_guard_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def cloud_guard_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def cloud_guard_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def cloud_guard_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def cloud_guard_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def cloud_guard_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def cloud_guard_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def cloud_guard_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def cloud_guard_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='cloud_guard',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def clusterplacementgroups_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def clusterplacementgroups_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def clusterplacementgroups_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def clusterplacementgroups_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def clusterplacementgroups_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def clusterplacementgroups_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def clusterplacementgroups_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def clusterplacementgroups_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def clusterplacementgroups_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='clusterplacementgroups',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def compute_cloud_at_customer_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def compute_cloud_at_customer_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def compute_cloud_at_customer_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def compute_cloud_at_customer_head(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def compute_cloud_at_customer_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def compute_cloud_at_customer_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def compute_cloud_at_customer_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def compute_cloud_at_customer_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def compute_cloud_at_customer_trace(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='compute_cloud_at_customer',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def container_instances_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def container_instances_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def container_instances_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def container_instances_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def container_instances_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def container_instances_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def container_instances_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def container_instances_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def container_instances_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='container_instances',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def containerengine_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def containerengine_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def containerengine_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def containerengine_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def containerengine_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def containerengine_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def containerengine_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def containerengine_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def containerengine_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='containerengine',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dashboard_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dashboard_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dashboard_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dashboard_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dashboard_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dashboard_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dashboard_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dashboard_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dashboard_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dashboard',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_catalog_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_catalog_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_catalog_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_catalog_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_catalog_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_catalog_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_catalog_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_catalog_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_catalog_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_catalog',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_flow_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_flow_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_flow_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_flow_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_flow_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_flow_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_flow_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_flow_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_flow_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_flow',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_integration_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_integration_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_integration_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_integration_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_integration_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_integration_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_integration_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_integration_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_integration_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_integration',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_safe_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_safe_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_safe_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_safe_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_safe_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_safe_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_safe_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_safe_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_safe_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_safe',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_science_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_science_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_science_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_science_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_science_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def data_science_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_science_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_science_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def data_science_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='data_science',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_management_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_management_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_management_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_management_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_management_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_management_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_management_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_management_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_management_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_management',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_migration_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_migration_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_migration_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_migration_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_migration_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_migration_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_migration_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_migration_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_migration_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_migration',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_tools_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_tools_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_tools_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_tools_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_tools_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def database_tools_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_tools_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_tools_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def database_tools_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='database_tools',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def datalabeling_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def datalabeling_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def datalabeling_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_dp_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_dp_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_dp_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_dp_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_dp_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def datalabeling_dp_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def datalabeling_dp_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def datalabeling_dp_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def datalabeling_dp_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='datalabeling_dp',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def delegate_access_control_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def delegate_access_control_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def delegate_access_control_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def delegate_access_control_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def delegate_access_control_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def delegate_access_control_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def delegate_access_control_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def delegate_access_control_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def delegate_access_control_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='delegate_access_control',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def devops_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='devops',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def devops_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='devops',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def devops_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='devops',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def devops_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='devops',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def devops_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='devops',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def devops_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='devops',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def devops_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='devops',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def devops_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='devops',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def devops_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='devops',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def digital_assistant_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def digital_assistant_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def digital_assistant_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def digital_assistant_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def digital_assistant_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def digital_assistant_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def digital_assistant_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def digital_assistant_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def digital_assistant_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='digital_assistant',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def disaster_recovery_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def disaster_recovery_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def disaster_recovery_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def disaster_recovery_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def disaster_recovery_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def disaster_recovery_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def disaster_recovery_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def disaster_recovery_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def disaster_recovery_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='disaster_recovery',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dms_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dms',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dms_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dms',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dms_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dms',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dms_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dms',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dms_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dms',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dms_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dms',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dms_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dms',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dms_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dms',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dms_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dms',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dns_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dns',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dns_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dns',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dns_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dns',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dns_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dns',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dns_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dns',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def dns_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dns',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dns_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dns',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dns_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='dns',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def dns_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='dns',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def document_understanding_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def document_understanding_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def document_understanding_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def document_understanding_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def document_understanding_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def document_understanding_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def document_understanding_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def document_understanding_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def document_understanding_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='document_understanding',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def edsfu_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def edsfu_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def edsfu_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def edsfu_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def edsfu_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def edsfu_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def edsfu_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def edsfu_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def edsfu_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='edsfu',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildelivery_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildelivery_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildelivery_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildelivery_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildelivery_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildelivery_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def emaildelivery_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def emaildelivery_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def emaildelivery_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildelivery',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildeliverysubmission_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildeliverysubmission_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildeliverysubmission_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildeliverysubmission_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildeliverysubmission_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def emaildeliverysubmission_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def emaildeliverysubmission_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def emaildeliverysubmission_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def emaildeliverysubmission_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='emaildeliverysubmission',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def events_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='events',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def events_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='events',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def events_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='events',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def events_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='events',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def events_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='events',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def events_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='events',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def events_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='events',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def events_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='events',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def events_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='events',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def filestorage_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def filestorage_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def filestorage_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def filestorage_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def filestorage_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def filestorage_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def filestorage_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def filestorage_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def filestorage_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='filestorage',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fleet_management_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fleet_management_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fleet_management_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fleet_management_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fleet_management_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fleet_management_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def fleet_management_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def fleet_management_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def fleet_management_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fleet_management',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functions_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functions',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functions_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functions',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functions_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functions',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functions_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functions',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functions_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functions',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functions_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='functions',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def functions_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='functions',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def functions_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='functions',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def functions_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functions',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functionsdocgenpbf_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functionsdocgenpbf_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functionsdocgenpbf_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functionsdocgenpbf_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functionsdocgenpbf_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def functionsdocgenpbf_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def functionsdocgenpbf_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def functionsdocgenpbf_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def functionsdocgenpbf_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='functionsdocgenpbf',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fusion_applications_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fusion_applications_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fusion_applications_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fusion_applications_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fusion_applications_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def fusion_applications_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def fusion_applications_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def fusion_applications_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def fusion_applications_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='fusion_applications',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_agents_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_agents_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_agents_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_agents',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_client_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_client_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_client_get(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_client_head(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_client_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_agents_client_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_agents_client_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_agents_client_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_agents_client_trace(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_agents_client',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_inference_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_inference_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_inference_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_inference_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_inference_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generative_ai_inference_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_inference_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_inference_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generative_ai_inference_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generative_ai_inference',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generic_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generic',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generic_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generic',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generic_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generic',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generic_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generic',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generic_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generic',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def generic_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generic',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generic_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generic',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generic_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='generic',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def generic_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='generic',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_get(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_head(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def globally_distributed_autonomous_database_trace(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='globally_distributed_autonomous_database',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def goldengate_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def goldengate_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def goldengate_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def goldengate_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def goldengate_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def goldengate_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def goldengate_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def goldengate_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def goldengate_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='goldengate',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def healthchecks_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def healthchecks_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def healthchecks_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def healthchecks_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def healthchecks_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def healthchecks_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def healthchecks_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def healthchecks_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def healthchecks_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='healthchecks',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def iaas_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def iaas_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def iaas_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def iaas_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def iaas_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def iaas_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def iaas_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def iaas_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def iaas_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='iaas',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_domains_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_domains_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_domains_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_domains_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_domains_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_domains_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_domains_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_domains_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_domains_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_domains',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_dp_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_dp_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_dp_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_dp_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_dp_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def identity_dp_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_dp_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_dp_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def identity_dp_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='identity_dp',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def incidentmanagement_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def incidentmanagement_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def incidentmanagement_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def incidentmanagement_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def incidentmanagement_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def incidentmanagement_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def incidentmanagement_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def incidentmanagement_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def incidentmanagement_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='incidentmanagement',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def instanceagent_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def instanceagent_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def instanceagent_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def instanceagent_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def instanceagent_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def instanceagent_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def instanceagent_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def instanceagent_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def instanceagent_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='instanceagent',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def integration_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='integration',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def integration_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='integration',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def integration_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='integration',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def integration_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='integration',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def integration_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='integration',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def integration_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='integration',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def integration_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='integration',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def integration_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='integration',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def integration_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='integration',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def itas_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='itas',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def itas_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='itas',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def itas_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='itas',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def itas_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='itas',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def itas_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='itas',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def itas_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='itas',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def itas_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='itas',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def itas_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='itas',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def itas_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='itas',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='jms',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def jms_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='jms',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def jms_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='jms',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def jms_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_java_download_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_java_download_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_java_download_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_java_download_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_java_download_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def jms_java_download_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def jms_java_download_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def jms_java_download_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def jms_java_download_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='jms_java_download',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def key_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='key',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def key_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='key',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def key_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='key',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def key_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='key',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def key_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='key',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def key_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='key',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def key_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='key',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def key_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='key',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def key_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='key',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def language_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='language',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def language_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='language',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def language_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='language',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def language_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='language',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def language_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='language',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def language_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='language',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def language_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='language',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def language_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='language',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def language_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='language',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def licensemanager_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def licensemanager_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def licensemanager_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def licensemanager_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def licensemanager_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def licensemanager_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def licensemanager_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def licensemanager_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def licensemanager_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='licensemanager',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def limits_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='limits',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def limits_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='limits',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def limits_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='limits',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def limits_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='limits',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def limits_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='limits',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def limits_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='limits',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def limits_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='limits',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def limits_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='limits',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def limits_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='limits',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def loadbalancer_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def loadbalancer_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def loadbalancer_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def loadbalancer_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def loadbalancer_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def loadbalancer_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def loadbalancer_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def loadbalancer_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def loadbalancer_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='loadbalancer',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logan_api_spec_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logan_api_spec_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logan_api_spec_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logan_api_spec_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logan_api_spec_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logan_api_spec_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logan_api_spec_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logan_api_spec_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logan_api_spec_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logan_api_spec',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_dataplane_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_dataplane_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_dataplane_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_dataplane_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_dataplane_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_dataplane_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_dataplane_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_dataplane_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_dataplane_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_dataplane',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_management_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_management_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_management_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_management_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_management_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_management_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_management_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_management_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_management_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_management',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_search_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_search_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_search_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_search_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_search_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def logging_search_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_search_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_search_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def logging_search_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='logging_search',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managed_access_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managed_access_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managed_access_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managed_access_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managed_access_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managed_access_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def managed_access_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def managed_access_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def managed_access_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managed_access',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def management_agent_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def management_agent_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def management_agent_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def management_agent_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def management_agent_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def management_agent_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def management_agent_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def management_agent_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def management_agent_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='management_agent',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managementdashboard_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managementdashboard_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managementdashboard_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managementdashboard_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managementdashboard_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def managementdashboard_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def managementdashboard_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def managementdashboard_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def managementdashboard_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='managementdashboard',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def marketplace_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def marketplace_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def marketplace_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def marketplace_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def marketplace_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def marketplace_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def marketplace_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def marketplace_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def marketplace_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='marketplace',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def monitoring_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def monitoring_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def monitoring_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def monitoring_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def monitoring_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def monitoring_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def monitoring_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def monitoring_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def monitoring_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='monitoring',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def mysql_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def mysql_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def mysql_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def mysql_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def mysql_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def mysql_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def mysql_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def mysql_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def mysql_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='mysql',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def network_firewall_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def network_firewall_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def network_firewall_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def network_firewall_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def network_firewall_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def network_firewall_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def network_firewall_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def network_firewall_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def network_firewall_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='network_firewall',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def networkloadbalancer_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def networkloadbalancer_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def networkloadbalancer_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def networkloadbalancer_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def networkloadbalancer_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def networkloadbalancer_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def networkloadbalancer_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def networkloadbalancer_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def networkloadbalancer_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='networkloadbalancer',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def nosql_database_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def nosql_database_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def nosql_database_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def nosql_database_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def nosql_database_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def nosql_database_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def nosql_database_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def nosql_database_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def nosql_database_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='nosql_database',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def notification_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='notification',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def notification_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='notification',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def notification_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='notification',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def notification_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='notification',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def notification_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='notification',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def notification_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='notification',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def notification_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='notification',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def notification_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='notification',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def notification_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='notification',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def objectstorage_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def objectstorage_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def objectstorage_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def objectstorage_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def objectstorage_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def objectstorage_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def objectstorage_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def objectstorage_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def objectstorage_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='objectstorage',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occ_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occ',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occ_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occ',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occ_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occ',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occ_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occ',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occ_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occ',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occ_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occ',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occ_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occ',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occ_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occ',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occ_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occ',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occcm_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occcm_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occcm_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occcm_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occcm_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occcm_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occcm_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occcm_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occcm_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occcm',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occds_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occds',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occds_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occds',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occds_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occds',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occds_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occds',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occds_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occds',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def occds_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occds',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occds_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occds',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occds_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='occds',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def occds_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='occds',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def oce_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='oce',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def oce_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='oce',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def oce_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='oce',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def oce_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='oce',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def oce_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='oce',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def oce_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='oce',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def oce_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='oce',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def oce_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='oce',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def oce_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='oce',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocicache_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocicache_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocicache_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocicache_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocicache_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocicache_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocicache_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocicache_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocicache_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocicache',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocm_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocm_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocm_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocm_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocm_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def ocm_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocm_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocm_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def ocm_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='ocm',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opa_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opa',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opa_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opa',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opa_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opa',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opa_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opa',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opa_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opa',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opa_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='opa',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def opa_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='opa',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def opa_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='opa',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def opa_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opa',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opensearch_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opensearch_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opensearch_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opensearch_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opensearch_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def opensearch_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def opensearch_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def opensearch_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def opensearch_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='opensearch',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operations_insights_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operations_insights_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operations_insights_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operations_insights_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operations_insights_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operations_insights_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def operations_insights_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def operations_insights_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def operations_insights_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operations_insights',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operatoraccesscontrol_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operatoraccesscontrol_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operatoraccesscontrol_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operatoraccesscontrol_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operatoraccesscontrol_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def operatoraccesscontrol_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def operatoraccesscontrol_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def operatoraccesscontrol_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def operatoraccesscontrol_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='operatoraccesscontrol',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def organizations_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def organizations_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def organizations_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def organizations_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def organizations_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def organizations_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def organizations_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def organizations_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def organizations_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='organizations',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def os_management_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def os_management_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def os_management_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def os_management_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def os_management_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def os_management_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def os_management_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def os_management_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def os_management_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='os_management',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def osmh_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def osmh_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def osmh_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def osmh_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def osmh_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def osmh_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def osmh_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def osmh_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def osmh_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='osmh',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def postgresql_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def postgresql_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def postgresql_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def postgresql_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def postgresql_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def postgresql_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def postgresql_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def postgresql_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def postgresql_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='postgresql',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def publisher_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def publisher_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def publisher_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def publisher_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def publisher_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def publisher_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def publisher_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def publisher_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def publisher_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='publisher',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def queue_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='queue',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def queue_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='queue',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def queue_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='queue',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def queue_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='queue',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def queue_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='queue',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def queue_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='queue',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def queue_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='queue',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def queue_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='queue',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def queue_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='queue',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def recovery_service_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def recovery_service_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def recovery_service_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def recovery_service_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def recovery_service_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def recovery_service_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def recovery_service_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def recovery_service_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def recovery_service_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='recovery_service',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def registry_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='registry',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def registry_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='registry',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def registry_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='registry',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def registry_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='registry',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def registry_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='registry',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def registry_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='registry',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def registry_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='registry',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def registry_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='registry',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def registry_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='registry',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_get(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_head(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resource_discovery_monitoring_control_api_trace(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='resource_discovery_monitoring_control_api',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_scheduler_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_scheduler_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_scheduler_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_scheduler_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_scheduler_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resource_scheduler_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resource_scheduler_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resource_scheduler_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resource_scheduler_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resource_scheduler',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resourcemanager_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resourcemanager_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resourcemanager_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resourcemanager_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resourcemanager_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def resourcemanager_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resourcemanager_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resourcemanager_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def resourcemanager_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='resourcemanager',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def rover_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='rover',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def rover_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='rover',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def rover_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='rover',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def rover_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='rover',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def rover_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='rover',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def rover_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='rover',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def rover_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='rover',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def rover_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='rover',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def rover_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='rover',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def s3objectstorage_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def s3objectstorage_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def s3objectstorage_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def s3objectstorage_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def s3objectstorage_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def s3objectstorage_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def s3objectstorage_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def s3objectstorage_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def s3objectstorage_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='s3objectstorage',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def scanning_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def scanning_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def scanning_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def scanning_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def scanning_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def scanning_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def scanning_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def scanning_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def scanning_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='scanning',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def search_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='search',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def search_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='search',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def search_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='search',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def search_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='search',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def search_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='search',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def search_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='search',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def search_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='search',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def search_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='search',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def search_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='search',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretmgmt_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretmgmt_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretmgmt_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretmgmt_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretmgmt_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretmgmt_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secretmgmt_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secretmgmt_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secretmgmt_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretmgmt',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretretrieval_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretretrieval_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretretrieval_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretretrieval_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretretrieval_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secretretrieval_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secretretrieval_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secretretrieval_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secretretrieval_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secretretrieval',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secure_desktops_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secure_desktops_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secure_desktops_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secure_desktops_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secure_desktops_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def secure_desktops_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secure_desktops_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secure_desktops_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def secure_desktops_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='secure_desktops',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def security_attribute_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def security_attribute_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def security_attribute_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def security_attribute_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def security_attribute_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def security_attribute_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def security_attribute_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def security_attribute_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def security_attribute_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='security_attribute',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_catalog_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_catalog_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_catalog_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_catalog_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_catalog_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_catalog_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def service_catalog_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def service_catalog_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def service_catalog_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_catalog',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_mesh_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_mesh_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_mesh_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_mesh_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_mesh_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def service_mesh_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def service_mesh_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def service_mesh_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def service_mesh_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='service_mesh',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def serviceconnectors_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def serviceconnectors_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def serviceconnectors_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def serviceconnectors_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def serviceconnectors_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def serviceconnectors_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def serviceconnectors_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def serviceconnectors_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def serviceconnectors_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='serviceconnectors',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def smp_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='smp',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def smp_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='smp',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def smp_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='smp',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def smp_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='smp',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def smp_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='smp',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def smp_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='smp',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def smp_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='smp',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def smp_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='smp',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def smp_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='smp',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def speech_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='speech',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def speech_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='speech',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def speech_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='speech',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def speech_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='speech',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def speech_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='speech',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def speech_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='speech',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def speech_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='speech',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def speech_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='speech',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def speech_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='speech',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def sqlwatch_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def sqlwatch_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def sqlwatch_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def sqlwatch_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def sqlwatch_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def sqlwatch_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def sqlwatch_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def sqlwatch_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def sqlwatch_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='sqlwatch',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def stack_monitoring_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def stack_monitoring_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def stack_monitoring_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def stack_monitoring_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def stack_monitoring_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def stack_monitoring_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def stack_monitoring_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def stack_monitoring_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def stack_monitoring_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='stack_monitoring',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def streaming_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def streaming_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def streaming_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def streaming_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def streaming_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def streaming_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def streaming_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def streaming_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def streaming_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='streaming',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def threat_intel_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def threat_intel_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def threat_intel_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def threat_intel_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def threat_intel_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def threat_intel_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def threat_intel_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def threat_intel_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def threat_intel_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='threat_intel',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='usage',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def usage_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='usage',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def usage_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='usage',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def usage_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_proxy_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_proxy_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_proxy_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_proxy_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_proxy_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def usage_proxy_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def usage_proxy_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def usage_proxy_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def usage_proxy_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='usage_proxy',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vision_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vision',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vision_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vision',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vision_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vision',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vision_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vision',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vision_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vision',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vision_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='vision',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def vision_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='vision',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def vision_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='vision',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def vision_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vision',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def visual_builder_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def visual_builder_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def visual_builder_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_studio_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_studio_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_studio_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_studio_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_studio_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def visual_builder_studio_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def visual_builder_studio_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def visual_builder_studio_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def visual_builder_studio_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='visual_builder_studio',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vmware_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vmware_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vmware_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vmware_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vmware_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def vmware_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def vmware_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def vmware_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def vmware_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='vmware',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waa_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waa',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waa_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waa',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waa_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waa',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waa_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waa',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waa_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waa',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waa_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waa',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waa_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waa',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waa_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waa',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waa_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waa',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waas_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waas',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waas_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waas',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waas_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waas',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waas_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waas',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waas_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waas',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waas_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waas',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waas_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waas',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waas_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waas',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waas_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waas',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waf_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waf',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waf_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waf',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waf_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waf',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waf_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waf',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waf_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waf',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def waf_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waf',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waf_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waf',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waf_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='waf',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def waf_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='waf',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def workrequests_connect(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def workrequests_delete(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def workrequests_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def workrequests_head(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def workrequests_options(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def workrequests_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def workrequests_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def workrequests_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def workrequests_trace(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='workrequests',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def zero_trust_packet_routing_connect(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.CONNECT,
            route=route,
            body=None,
            output_file=output_file,
        )

    def zero_trust_packet_routing_delete(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.DELETE,
            route=route,
            body=None,
            output_file=output_file,
        )

    def zero_trust_packet_routing_get(self, route: str, output_file: typing.BinaryIO | None = None):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.GET,
            route=route,
            body=None,
            output_file=output_file,
        )

    def zero_trust_packet_routing_head(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.HEAD,
            route=route,
            body=None,
            output_file=output_file,
        )

    def zero_trust_packet_routing_options(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.OPTIONS,
            route=route,
            body=None,
            output_file=output_file,
        )

    def zero_trust_packet_routing_patch(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.PATCH,
            route=route,
            body=body,
            output_file=output_file,
        )

    def zero_trust_packet_routing_post(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.POST,
            route=route,
            body=body,
            output_file=output_file,
        )

    def zero_trust_packet_routing_put(
        self,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None = None,
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.PUT,
            route=route,
            body=body,
            output_file=output_file,
        )

    def zero_trust_packet_routing_trace(
        self, route: str, output_file: typing.BinaryIO | None = None
    ):
        return self.request(
            service='zero_trust_packet_routing',
            method=_client.HttpMethod.TRACE,
            route=route,
            body=None,
            output_file=output_file,
        )
