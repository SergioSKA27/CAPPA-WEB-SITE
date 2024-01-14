from streamlit_elements import mui
from .dashboard import Dashboard


# The `Card` class represents a card component with a title, subheader, image, content, and action buttons.
class Timer(Dashboard.Item):

    DEFAULT_CONTENT = (
        "This impressive paella is a perfect party dish and a fun meal to cook "
        "together with your guests. Add 1 cup of frozen peas along with the mussels, "
        "if you like."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dark_mode = False

    def __call__(self,output=None,time=None,current=None,peak=None):
        """
        The function creates a card component with a title, subheader, image, content, and action buttons.

        :param content: The `content` parameter is the text or content that will be displayed in the `CardContent` component
        of the card
        """
        if output is None:
            output=["",""]
        if time is None:
            time="0"
        if current is None:
            current=0
        if peak is None:
            peak=0



        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar("0px 15px 0px 15px",dark_switcher=False):
                mui.icon.Code()
                mui.Typography("Entorno de ejecución", sx={"fontSize": "1.2rem"})
            mui.Divider()
            with mui.Box(
                sx={
                    "display": "flex",
                    "flexDirection": "row",
                    "alignItems": "center",
                    "padding": "0px 15px 0px 15px",
                    "backgroundColor": "#36A0A0",
                    "color": "#FFFFFF",
                    "borderRadius": 3,
                }
            ):
                mui.icon.Terminal()
                mui.Typography("Salida", sx={"paddingLeft": "10px", "fontSize": "1.2rem"})

            mui.Divider()
            mui.Typography(output[0], sx={"padding": "10px"})
            mui.Typography(output[1], sx={"padding": "10px","color":"#FF0000"})

            with mui.Box(
                sx={
                    "display": "flex",
                    "flexDirection": "row",
                    "alignItems": "center",
                    "padding": "0px 15px 0px 15px",
                    "backgroundColor": "#36A0A0",
                    "color": "#FFFFFF",
                    "borderRadius": 3,
                }
            ):
                mui.icon.Timer()
                mui.Typography("Tiempo de ejecución", sx={"paddingLeft": "10px", "fontSize": "1.2rem"})
            mui.Divider()
            mui.Typography(time+" s", sx={"padding": "10px"})

            with mui.Box(
                sx={
                    "display": "flex",
                    "flexDirection": "row",
                    "alignItems": "center",
                    "padding": "0px 15px 0px 15px",
                    "backgroundColor": "#36A0A0",
                    "color": "#FFFFFF",
                    "borderRadius": 3,
                }
            ):
                mui.icon.Memory()
                mui.Typography("Memoria", sx={"paddingLeft": "10px", "fontSize": "1.2rem"})
            mui.Divider()
            mui.Typography(f"Memoria Utilizada:\t\t {current / 10**6:.6f} MB \n")
            mui.Typography(f"Memoria Pico:\t\t {peak / 10**6:.6f} MB \n")

