import asyncio
from collections import deque
from .data_visualization import DataVisualizationApp
from .graph_udp_server import start_udp_server


async def main_graph_runner_core(
    port=12750,
    deque_length=250,
    interval=100,
    title="Real-Time Data Visualization",
    y_label="",
):
    # if interval < 100 throw an error
    if interval < 100:
        print("Graph update interval should be greater than 100")
        return

    data_app = DataVisualizationApp(title=title, y_label=y_label, interval=interval)
    data_app.data_queue = deque(maxlen=deque_length)

    dash_task = asyncio.to_thread(data_app.run)
    udp_task = start_udp_server(data_app, port=port)

    await asyncio.gather(dash_task, udp_task)


def main_graph_runner(
    port=12750,
    deque_length=250,
    interval=100,
    title="Real-Time Data Visualization",
    y_label="",
):
    asyncio.run(
        main_graph_runner_core(
            port=12750,
            deque_length=250,
            interval=200,
            title="Real-Time Data Visualization",
            y_label=y_label,
        )
    )


if __name__ == "__main__":
    main_graph_runner()
