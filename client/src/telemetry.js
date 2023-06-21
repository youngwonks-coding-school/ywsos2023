import { context, trace } from '@opentelemetry/api';
import {
    SimpleSpanProcessor,
    ConsoleSpanExporter
} from '@opentelemetry/sdk-trace-base';
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import axios from 'axios';

class ServerSpanExporter extends ConsoleSpanExporter {
    export(spans) {
        for (const span of spans) {
            let toSendSpan = {
                attributes: span.attributes,
                endTime: span.endTime,
                events: span.events,
                startTime: span.startTime,
                name: span.name,
            }
            axios.post('/api/web-telemetry', toSendSpan);
        }
    }
}

const provider = new WebTracerProvider();
provider.addSpanProcessor(new SimpleSpanProcessor(new ServerSpanExporter()));

provider.register({
    contextManager: new ZoneContextManager(),
});

const webTracerWithZone = provider.getTracer();

export {trace, context, webTracerWithZone}
