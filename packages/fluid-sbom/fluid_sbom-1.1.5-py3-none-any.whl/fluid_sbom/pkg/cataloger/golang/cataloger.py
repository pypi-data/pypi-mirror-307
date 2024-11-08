from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fluid_sbom.pkg.cataloger.golang.parse_go_mod import (
    parse_go_mod,
)
from fnmatch import (
    fnmatch,
)
import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)


def on_next_golang(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            try:
                if any(
                    fnmatch(value, x)
                    for x in (
                        "**/go.mod",
                        "go.mod",
                    )
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_go_mod,
                            parser_name="parse-go-mod",
                        )
                    )

            except Exception as ex:  # pylint:disable=broad-exception-caught
                observer.on_error(ex)

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
