class Broadcaster:
    def __init__(self, name):
        self.name = name
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)
        listener.register_sender(self)

    def broadcast(self, pulse):
        return [(self.name, listener.name, pulse) for listener in self.listeners]
    
    def __repr__(self) -> str:
        return f"{self.name} -> {self.listeners}"

class PulseSink:
    def __init__(self, name):
        self.name = name
        self.high_pulse_count = 0
        self.low_pulse_count = 0
        self.senders = []

    def register_sender(self, sender):
        self.senders.append(sender)
        pass
    
    def notify(self, pulse, sender):
        if pulse == 1:
            self.high_pulse_count += 1
        else:
            self.low_pulse_count += 1
        return []
    
    def __repr__(self) -> str:
        return f"Sink {self.name} High: {self.high_pulse_count} Low: {self.low_pulse_count}"

class FlipFlopModule:
    def __init__(self, name):
        self.name = name
        self.last_state = False
        self.listeners = []
        self.senders = []

    def register(self, listener):
        self.listeners.append(listener)
        listener.register_sender(self)

    def register_sender(self, sender):
        self.senders.append(sender)
        pass
        
    def notify(self, pulse, sender):
        # Received a high pulse = nothing happens
        if pulse == 1:
            return []
        
        self.last_state = not self.last_state
        result = []
        # If it was off, it turns on and sends a high pulse
        if self.last_state:
            send_val = 1
        # If it was on, it turns off and sends a low pulse.
        else:
            send_val = 0
        for listener in self.listeners:
            result.append((self.name, listener.name, send_val))

        return result
    
    def __repr__(self) -> str:
        return f"FlipFlop {self.name} -> {self.listeners}"

class ConjunctionModule:
    def __init__(self, name):
        self.name = name
        self.last_state = False
        self.listeners = []
        self.received_pulses = {}
        self.senders = []

    def register(self, listener):
        self.listeners.append(listener)
        listener.register_sender(self)
        
    def register_sender(self, sender):
        self.senders.append(sender)
        if sender not in self.received_pulses:
            self.received_pulses[sender.name] = 0

    def notify(self, pulse, sender):
        # Conjunction modules initially default to remembering a low pulse for each input
        if sender not in self.received_pulses:
            self.received_pulses[sender] = 0

        # When a pulse is received, the conjunction module first updates its memory for that input.
        self.received_pulses[sender] = pulse

        # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends 
        # a high pulse.
        if all([pulse == 1 for pulse in self.received_pulses.values()]):
            return [(self.name, listener.name, 0) for listener in self.listeners]
        else:
            return [(self.name, listener.name, 1) for listener in self.listeners]

    def __repr__(self) -> str:
        return f"Conjunction {self.name} -> {self.listeners}"

lines = [l.strip() for l in open('Inputs/day20.txt').readlines() if l.strip() != '']

def load_modules(lines):
    result = {}
    # First pass - create all modules
    for l in lines:
        parts = l.split(' -> ')
        if parts[0].startswith('&') or parts[0].startswith('%'):        
            name = parts[0][1:]
            if parts[0].startswith('&'):
                module = ConjunctionModule(name)
            else:
                module = FlipFlopModule(name)
            result[name] = module
        else:
            name = parts[0]
            module = Broadcaster(name)
            result[name] = module

    # Second pass - wire them up
    for l in lines:
        parts = l.split(' -> ')
        if parts[0].startswith('&') or parts[0].startswith('%'):        
            name = parts[0][1:]
        else:
            name = parts[0]
        listeners = parts[1].split(', ')
        for listener in listeners:
            if not listener in result:
                result[listener] = PulseSink(listener)
            result[name].register(result[listener])
    return result

modules = load_modules(lines)

def broadcast(pulse, modules):
    low_pulses = 1
    high_pulses = 0
    #print(f"button -low-> broadcaster")
    broadcaster = modules['broadcaster'] 
    broadcast_stack = broadcaster.broadcast(pulse)
    while len(broadcast_stack) > 0:
        item = broadcast_stack.pop(0)
        
        sender, receiver, pulse = item
        # print(f"{sender} -{pulse}-> {receiver}")
        if pulse == 1:
            high_pulses += 1
        else:
            low_pulses += 1
        broadcast_stack.extend(modules[receiver].notify(pulse, sender))
    return low_pulses, high_pulses

# Send one thousand pulses through the system
total_low_pulse = 0
total_high_pulse = 0
for i in range(1000):
    low_pulse, high_pulse = broadcast(0, modules)
    total_low_pulse += low_pulse
    total_high_pulse += high_pulse

print("Part 1", (total_low_pulse) * (total_high_pulse))


# Part 2
part2_modules = load_modules(lines)


for x in range(1000000):
    broadcast(0, part2_modules)

rx_writers = part2_modules["rx"].senders

print("Part 2", 15)
    