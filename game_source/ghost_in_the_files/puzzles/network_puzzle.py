import pygame
import math
from settings import program_width, program_height, program_header_height
from entities.game_state import GameState
from entities.programs.program_window import ProgramWindow
from entities.items.key import Key

class Node():
    def __init__(self, name, pos, empty_node_sprite, active_node_sprite, null_node_sprite, null_empty_node_sprite):
        self.name = name
        self.pos = pos
        
        self.empty_node_sprite = empty_node_sprite
        self.active_node_sprite = active_node_sprite

        self.null_node_sprite = null_node_sprite
        self.null_empty_node_sprite = null_empty_node_sprite
        
        self.active = False
        self.connections = []
        self.font = pygame.font.SysFont(None, 28)
     
    def render(self, screen):
        if not self.name == "null":
            sprite = self.active_node_sprite if self.active else self.empty_node_sprite
            rect = sprite.get_rect(center = self.pos)
            screen.blit(sprite, rect.topleft)
        else:
            screen.blit(self.null_empty_node_sprite, self.null_empty_node_sprite.get_rect(center = self.pos).topleft)
            if GameState.network_puzzle_state["item_used"] == True:
                screen.blit(self.null_node_sprite, self.null_node_sprite.get_rect(center = self.pos).topleft)            
        
        if self.name == "null":
            return
        label = self.font.render(self.name, True, (255, 255, 255))
        label_rect = label.get_rect(midleft=self.pos) if self.pos[0] < screen.get_width() / 2 else label.get_rect(midright=self.pos)
        
        if self.pos[0] < screen.get_width() / 2:
            label_rect.right = self.pos[0] - 45
        else:
            label_rect.left = self.pos[0] + 45
        screen.blit(label, label_rect.topleft)

class Edge():
    def __init__(self, from_node, to_node, empty_edge_sprite, full_edge_sprite):
        self.from_node = from_node
        self.to_node = to_node
       
        if from_node.name == "null":
            from_radius = from_node.null_empty_node_sprite.get_width() / 2
        else:
            from_radius = from_node.empty_node_sprite.get_width() / 2

        if to_node.name == "null":
            to_radius = to_node.null_empty_node_sprite.get_width() / 2
        else:
            to_radius = to_node.empty_node_sprite.get_width() / 2
        
        dx, dy = to_node.pos[0] - from_node.pos[0], to_node.pos[1] - from_node.pos[1]
        length = math.hypot(dx, dy)
        
        self.start = (from_node.pos[0] + dx / length * from_radius, from_node.pos[1] + dy / length * to_radius)
        self.end = (to_node.pos[0] - dx / length * from_radius, to_node.pos[1] - dy / length * to_radius)
        
        self.length = math.hypot(self.end[0] - self.start[0], self.end[1] - self.start[1])
        self.angle = -math.degrees(math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0]))
        self.center = ((self.start[0] + self.end[0]) / 2, (self.start[1] + self.end[1]) / 2)
        
        self.empty_edge_sprite = empty_edge_sprite
        self.empty_edge_sprite = pygame.transform.scale(self.empty_edge_sprite, (self.length, 10))
        self.empty_edge_sprite = pygame.transform.rotate(self.empty_edge_sprite, self.angle)
        
        self.full_edge_sprite = full_edge_sprite
        self.full_edge_sprite = pygame.transform.scale(self.full_edge_sprite, (self.length, 10))
        self.full_edge_sprite = pygame.transform.rotate(self.full_edge_sprite, self.angle)
        self.active = False
    
    def click(self, mouse_pos):
        length = (self.end[0] - self.start[0]) ** 2 + (self.end[1] - self.start[1]) ** 2
        t = max(0, min(1, ((mouse_pos[0] - self.start[0]) * (self.end[0] - self.start[0]) + (mouse_pos[1] - self.start[1]) * (self.end[1] - self.start[1])) / length))
        x = self.start[0] + t * (self.end[0] - self.start[0])
        y = self.start[1] + t * (self.end[1] - self.start[1])
        distance = (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2
        return distance < 12 ** 2
    
    def render(self, screen):
        sprite = self.full_edge_sprite if self.active else self.empty_edge_sprite
        rect = sprite.get_rect(center = self.center)
        screen.blit(sprite, rect.topleft)
 
class NetworkPuzzle():
    def __init__(self, screen, inventory):
        self.screen = screen
        self.inventory = inventory
        
        self.window = ProgramWindow(
            "NetworkPuzzle",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        ) 
        
        self.empty_node_sprite = pygame.image.load("assets/sprites/nodes/empty_node.png")
        self.empty_node_sprite = pygame.transform.scale(self.empty_node_sprite, (60, 60))
        
        self.active_node_sprite = pygame.image.load("assets/sprites/nodes/active_node.png")
        self.active_node_sprite = pygame.transform.scale(self.active_node_sprite, (60, 60))
        
        self.null_node_sprite = pygame.image.load("assets/sprites/nodes/null_node.png")
        self.null_node_sprite = pygame.transform.scale(self.null_node_sprite, (50, 50))
        
        self.null_empty_node_sprite = pygame.image.load("assets/sprites/nodes/null_empty_node.png")
        self.null_empty_node_sprite = pygame.transform.scale(self.null_empty_node_sprite, (60, 60))
        
        self.empty_edge_sprite = pygame.image.load("assets/sprites/edges/empty_edge.png")
        self.active_edge_sprite = pygame.image.load("assets/sprites/edges/active_edge.png")
        
        self.x = self.window.x + program_width / 2
        self.y = self.window.y + program_height / 2 + program_header_height - 5
        
        self.key_sprite = pygame.image.load("assets/sprites/items/key.png")
        self.key_sprite = pygame.transform.scale(self.key_sprite, (40, 40))
        self.key_rect = self.key_sprite.get_rect(topleft=(self.x - 20, self.y - 20))
        
        node_names = ["null", "A", "B", "C", "D"]
        radius = 165
        self.nodes = {}
        for i, name in enumerate(node_names):
            angle = i * (2 * math.pi / len(node_names)) - math.pi / 2
            x = radius * math.cos(angle) + self.x
            y = radius * math.sin(angle) + self.y
            self.nodes[name] = Node(name, (x, y), self.empty_node_sprite, self.active_node_sprite, self.null_node_sprite, self.null_empty_node_sprite)
            self.nodes[name].active = GameState.network_puzzle_state["nodes"].get(name, False)
        
        self.edges = []
        node_names = list(self.nodes.keys())
        for i in range(len(node_names)):
            for j in range(i + 1, len(node_names)):
                edge = Edge(self.nodes[node_names[i]], self.nodes[node_names[j]], self.empty_edge_sprite, self.active_edge_sprite)
                edge.active = GameState.network_puzzle_state["edges"].get((node_names[i], node_names[j]), False)
                self.edges.append(edge)
                self.nodes[node_names[i]].connections.append(edge)
                self.nodes[node_names[j]].connections.append(edge)
    
    def on_item_use(self, item, null_node):
        if item.name.lower() == "null pointer":
            self.inventory.remove_item(item)
            GameState.network_puzzle_state["item_used"] = True
            null_node.active = True
            self.save_graph()

            if self.check_win():
                GameState.network_puzzle_state["win"] = True
                for node in self.nodes.values():
                    node.active = True
                GameState.add_log("[SYSTEM] Data pathways fully restored. Network operational.")
    
    def check_win(self):
        winning_edges = {("D", "C"), ("C", "null"), ("D", "B"), ("D", "A"), ("A", "B"), ("A", "null")}
        
        active_edges = set()
        for edge in self.edges:
            if edge.active:
                active_edges.add(tuple(sorted([edge.from_node.name, edge.to_node.name])))
        
        return active_edges == {tuple(sorted(edge)) for edge in winning_edges} and GameState.network_puzzle_state["item_used"] == True
    
    def save_graph(self):
        GameState.network_puzzle_state["nodes"] = {name: node.active for name, node in self.nodes.items()}
        GameState.network_puzzle_state["edges"] = {
            (edge.from_node.name, edge.to_node.name): edge.active for edge in self.edges
        }
    
    def handle_event(self, event):
        if not self.window.active:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if GameState.network_puzzle_state["win"] == True and GameState.network_puzzle_state["reward_given"] == False:
                if self.key_rect.collidepoint(mouse_pos):
                    GameState.network_puzzle_state["reward_given"] = True
                    key = Key(slot_size = self.inventory.slot_size)
                    self.inventory.add_item(key)
            
            if GameState.network_puzzle_state["win"] == True:
                return

            if GameState.network_puzzle_state["item_used"] == False:
                null_node = self.nodes["null"]
                null_node_rect = null_node.null_empty_node_sprite.get_rect(center = null_node.pos)
                
                if null_node_rect.collidepoint(mouse_pos):
                    if self.inventory.hovered_slot is not None and self.inventory.hovered_slot < len(self.inventory.items):
                            item = self.inventory.items[self.inventory.hovered_slot]
                            if isinstance(item, type(None)) is False:
                                self.on_item_use(item, null_node)
            
            for edge in self.edges:
                if edge.click(event.pos):
                    edge.active = not edge.active
                    self.save_graph()
                    
                    if self.check_win():
                        GameState.network_puzzle_state["win"] = True
                        for node in self.nodes.values():
                            node.active = True

    
    def update(self):
        pass
    
    def render(self, rect):
        if not self.window.active:
            return
                
        for edge in self.edges:
            edge.render(self.screen)
        
        for node in self.nodes.values():
            node.render(self.screen)
        
        if GameState.network_puzzle_state["win"] == True and GameState.network_puzzle_state["reward_given"] == False:
            self.screen.blit(self.key_sprite, self.key_rect)
