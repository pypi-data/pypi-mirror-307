from typing import Literal
from quantplay.broker.xts import XTS


class Jainam(XTS):
    def __init__(
        self,
        api_secret: str | None = None,
        api_key: str | None = None,
        md_api_key: str | None = None,
        md_api_secret: str | None = None,
        wrapper: str | None = None,
        md_wrapper: str | None = None,
        client_id: str | None = None,
        load_instrument: bool = True,
        is_dealer: bool = False,
        XTS_type: Literal["A", "B"] = "A",
    ) -> None:
        super().__init__(
            root_url=f"http://ctrade.jainam.in:{3000 if XTS_type == 'A' else 3001}",
            api_key=api_key,
            api_secret=api_secret,
            md_api_key=md_api_key,
            md_api_secret=md_api_secret,
            wrapper=wrapper,
            md_wrapper=md_wrapper,
            ClientID=client_id,
            is_dealer=is_dealer,
            load_instrument=load_instrument,
        )

        if is_dealer:
            self.ClientID = "*****"
