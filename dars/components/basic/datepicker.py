from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable
from datetime import datetime, date

class DatePicker(Component):
    def __init__(
        self,
        value: Optional[Union[str, date, datetime]] = None,
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        placeholder: str = "Seleccionar fecha",
        format: str = "YYYY-MM-DD",  # Formato de fecha
        locale: str = "es",  # Idioma para el picker
        show_time: bool = False,  # Si incluir selector de tiempo
        inline: bool = False,  # Si mostrar inline o como popup
        disabled_dates: Optional[list] = None,  # Fechas deshabilitadas
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        disabled: bool = False,
        required: bool = False,
        readonly: bool = False,
        on_change: Optional[Callable] = None,
        on_open: Optional[Callable] = None,
        on_close: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        
        # Asignar atributos básicos primero
        self.placeholder = placeholder
        self.format = format
        self.locale = locale
        self.show_time = show_time
        self.inline = inline
        self.disabled_dates = disabled_dates or []
        self.disabled = disabled
        self.required = required
        self.readonly = readonly
        
        # Validar formato
        valid_formats = ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY", "DD-MM-YYYY"]
        if format not in valid_formats:
            raise ValueError(f"format debe ser uno de: {valid_formats}")
        
        # Validar locale
        valid_locales = ["es", "en", "fr", "de", "it", "pt"]
        if locale not in valid_locales:
            raise ValueError(f"locale debe ser uno de: {valid_locales}")
        
        # Ahora procesar las fechas (después de asignar self.format)
        self.value = self._process_date(value)
        self.min_date = self._process_date(min_date)
        self.max_date = self._process_date(max_date)
        
        # Registrar eventos si se proporcionan
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)
        if on_open:
            self.set_event("open", on_open)
        if on_close:
            self.set_event("close", on_close)
    
    def _process_date(self, date_value: Optional[Union[str, date, datetime]]) -> Optional[str]:
        """Procesa y normaliza el valor de fecha"""
        if date_value is None:
            return None
        
        if isinstance(date_value, str):
            # Validar formato de string de fecha
            try:
                # Intentar parsear la fecha para validarla
                if self.format == "YYYY-MM-DD":
                    datetime.strptime(date_value, "%Y-%m-%d")
                elif self.format == "DD/MM/YYYY":
                    datetime.strptime(date_value, "%d/%m/%Y")
                elif self.format == "MM/DD/YYYY":
                    datetime.strptime(date_value, "%m/%d/%Y")
                elif self.format == "DD-MM-YYYY":
                    datetime.strptime(date_value, "%d-%m-%Y")
                return date_value
            except ValueError:
                raise ValueError(f"Formato de fecha inválido: {date_value}")
        
        elif isinstance(date_value, (date, datetime)):
            # Convertir objeto date/datetime a string según el formato
            if self.format == "YYYY-MM-DD":
                return date_value.strftime("%Y-%m-%d")
            elif self.format == "DD/MM/YYYY":
                return date_value.strftime("%d/%m/%Y")
            elif self.format == "MM/DD/YYYY":
                return date_value.strftime("%m/%d/%Y")
            elif self.format == "DD-MM-YYYY":
                return date_value.strftime("%d-%m-%Y")
        
        return str(date_value)
    
    def set_value(self, value: Union[str, date, datetime]):
        """Establece el valor de la fecha"""
        self.value = self._process_date(value)
    
    def get_date_object(self) -> Optional[datetime]:
        """Obtiene el valor como objeto datetime"""
        if not self.value:
            return None
        
        try:
            if self.format == "YYYY-MM-DD":
                return datetime.strptime(self.value, "%Y-%m-%d")
            elif self.format == "DD/MM/YYYY":
                return datetime.strptime(self.value, "%d/%m/%Y")
            elif self.format == "MM/DD/YYYY":
                return datetime.strptime(self.value, "%m/%d/%Y")
            elif self.format == "DD-MM-YYYY":
                return datetime.strptime(self.value, "%d-%m-%Y")
        except ValueError:
            return None
    
    def is_date_disabled(self, date_to_check: Union[str, date, datetime]) -> bool:
        """Verifica si una fecha está deshabilitada"""
        check_date = self._process_date(date_to_check)
        return check_date in self.disabled_dates
    
    def add_disabled_date(self, date_to_disable: Union[str, date, datetime]):
        """Añade una fecha a la lista de fechas deshabilitadas"""
        disabled_date = self._process_date(date_to_disable)
        if disabled_date and disabled_date not in self.disabled_dates:
            self.disabled_dates.append(disabled_date)
    
    def remove_disabled_date(self, date_to_enable: Union[str, date, datetime]):
        """Elimina una fecha de la lista de fechas deshabilitadas"""
        enabled_date = self._process_date(date_to_enable)
        if enabled_date in self.disabled_dates:
            self.disabled_dates.remove(enabled_date)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")
