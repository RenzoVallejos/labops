from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Tree, Static
from textual.binding import Binding
from api_client import get_hosts, get_racks, get_k2_ip

class LabOpsTUI(App):
    """LabOps Terminal User Interface"""
    
    TITLE = "LabOps - Datacenter Lab Management"
    CSS = """
    #left_panel {
        width: 40%;
        border: solid $primary;
    }
    
    #right_panel {
        width: 60%;
        border: solid $primary;
        padding: 1;
    }
    
    #rack_tree {
        height: 100%;
    }
    
    #rack_details {
        height: 100%;
        overflow-y: auto;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Container(
                Tree("SEALAB85 Racks", id="rack_tree"),
                id="left_panel"
            ),
            Container(
                Static("Select a rack to view details", id="rack_details"),
                id="right_panel"
            ),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Load initial data"""
        self.load_racks_tree()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle room, rack, host, or more selection"""
        node = event.node
        if hasattr(node.data, 'get'):
            if node.data.get('type') == 'room':
                self.show_room_details(node.data['room'])
            elif node.data.get('type') == 'rack':
                self.show_rack_details(node.data['rack'])
            elif node.data.get('type') == 'host':
                self.show_host_details(node.data['host'])
            elif node.data.get('type') == 'more':
                self.expand_more_hosts(node)

    def load_racks_tree(self) -> None:
        """Load racks into tree view grouped by room"""
        try:
            tree = self.query_one("#rack_tree", Tree)
            tree.clear()
            
            racks = get_racks()
            
            # Group racks by room (e.g., SEA85.159, SEA85.6920)
            rooms = {}
            for rack in racks:
                position = rack.get('position', '')
                # Extract room from position (e.g., SEA85.159.R6-L01 -> SEA85.159)
                if '.' in position:
                    parts = position.split('.')
                    if len(parts) >= 2:
                        room = f"{parts[0]}.{parts[1]}"  # SEA85.159
                    else:
                        room = parts[0]  # Fallback
                else:
                    room = "Unknown"
                
                if room not in rooms:
                    rooms[room] = []
                rooms[room].append(rack)
            
            # Add room nodes to tree
            for room_name, room_racks in sorted(rooms.items()):
                total_hosts = sum(r.get('host_count', 0) for r in room_racks)
                room_node = tree.root.add(
                    f"{room_name} ({len(room_racks)} racks, {total_hosts} hosts)",
                    data={'type': 'room', 'room': room_name}
                )
                
                # Add rack children
                for rack in sorted(room_racks, key=lambda x: x.get('position', '')):
                    host_count = rack.get('host_count', 0)
                    status_text = f"({host_count} hosts)" if host_count > 0 else "(Empty)"
                    
                    rack_node = room_node.add(
                        f"{rack.get('position', 'Unknown')} {status_text}",
                        data={'type': 'rack', 'rack': rack}
                    )
                    
                    # Add host children if rack has hosts (limit display to 5 for tree view)
                    if host_count > 0 and rack.get('hosts'):
                        for host in rack['hosts'][:5]:  # Show first 5 hosts in tree
                            asset_id = host.get('assetid', 'N/A')
                            platform = host.get('platform', 'Unknown')
                            status = host.get('status', 'Unknown')
                            
                            rack_node.add_leaf(
                                f"{asset_id}: {platform} [{status}]",
                                data={'type': 'host', 'host': host}
                            )
                        
                        # Add "..." indicator if there are more hosts
                        if len(rack['hosts']) > 5:
                            rack_node.add_leaf(
                                f"... and {len(rack['hosts']) - 5} more hosts",
                                data={'type': 'more', 'rack': rack, 'rack_node': rack_node}
                            )
            
        except Exception as e:
            details = self.query_one("#rack_details", Static)
            details.update(f"Error loading racks: {e}")

    def show_rack_details(self, rack) -> None:
        """Show detailed rack information"""
        details = self.query_one("#rack_details", Static)
        
        rack_info = []
        rack_info.append(f"Rack: {rack.get('position', 'Unknown')}")
        rack_info.append(f"Lab: {rack.get('lab', 'Unknown')}")
        rack_info.append(f"Host Count: {rack.get('host_count', 0)}")
        rack_info.append("")
        
        if rack.get('hosts'):
            rack_info.append(f"Hosts in Rack ({len(rack['hosts'])}):")  # Show actual count
            for host in rack['hosts']:  # Show ALL hosts, not limited
                asset_id = host.get('assetid', 'N/A')
                platform = host.get('platform', 'Unknown')
                status = host.get('status', 'Unknown')
                con_ip = host.get('con_ip', 'N/A')
                
                rack_info.append(f"  • {asset_id}: {platform} [{status}]")
                if con_ip != 'N/A':
                    rack_info.append(f"    Console IP: {con_ip}")
                rack_info.append("")
        
        details.update("\n".join(rack_info))

    def show_host_details(self, host) -> None:
        """Show detailed host information"""
        details = self.query_one("#rack_details", Static)
        
        host_info = []
        host_info.append(f"Asset ID: {host.get('assetid', 'N/A')}")
        host_info.append(f"Platform: {host.get('platform', 'Unknown')}")
        host_info.append(f"Status: {host.get('status', 'Unknown')}")
        host_info.append(f"Location: {host.get('location', 'N/A')}")
        host_info.append("")
        
        # Hardware info
        if host.get('hardwareid'):
            host_info.append(f"Hardware ID: {host.get('hardwareid')}")
        
        # Network info
        host_info.append("Network Information:")
        if host.get('con_ip'):
            host_info.append(f"  Console IP: {host.get('con_ip')}")
        else:
            host_info.append("  Console IP: N/A")
        
        # Get K2 IP if hardware ID is available
        k2_ip = 'N/A'
        if host.get('hardwareid'):
            k2_result = get_k2_ip(host.get('hardwareid'))
            if k2_result:
                k2_ip = k2_result
        
        host_info.append(f"  K2 IP: {k2_ip}")
            
        if host.get('lan_ip'):
            host_info.append(f"  LAN IP: {host.get('lan_ip')}")
        else:
            host_info.append("  LAN IP: N/A")
        
        host_info.append("")
        host_info.append("Click on rack name to go back to rack view")
        
        details.update("\n".join(host_info))

    def show_room_details(self, room_name) -> None:
        """Show room summary information"""
        details = self.query_one("#rack_details", Static)
        
        try:
            racks = get_racks()
            room_racks = [r for r in racks if r.get('position', '').startswith(room_name)]
            
            room_info = []
            room_info.append(f"Room: {room_name}")
            room_info.append(f"Total Racks: {len(room_racks)}")
            
            total_hosts = sum(r.get('host_count', 0) for r in room_racks)
            room_info.append(f"Total Hosts: {total_hosts}")
            room_info.append("")
            
            if room_racks:
                room_info.append("Racks in Room:")
                for rack in sorted(room_racks, key=lambda x: x.get('position', '')):
                    host_count = rack.get('host_count', 0)
                    status = f"({host_count} hosts)" if host_count > 0 else "(Empty)"
                    room_info.append(f"  • {rack.get('position')} {status}")
            
            room_info.append("")
            room_info.append("Expand room to see individual racks")
            
            details.update("\n".join(room_info))
            
        except Exception as e:
            details.update(f"Error loading room details: {e}")

    def expand_more_hosts(self, more_node) -> None:
        """Expand the remaining hosts in the tree"""
        try:
            rack = more_node.data['rack']
            rack_node = more_node.parent  # Get the rack node
            
            # Remove the "more" node
            more_node.remove()
            
            # Add the remaining hosts (from index 5 onwards)
            if rack.get('hosts') and len(rack['hosts']) > 5:
                for host in rack['hosts'][5:]:  # Show remaining hosts
                    asset_id = host.get('assetid', 'N/A')
                    platform = host.get('platform', 'Unknown')
                    status = host.get('status', 'Unknown')
                    
                    rack_node.add_leaf(
                        f"{asset_id}: {platform} [{status}]",
                        data={'type': 'host', 'host': host}
                    )
            
        except Exception as e:
            details = self.query_one("#rack_details", Static)
            details.update(f"Error expanding hosts: {e}")



if __name__ == "__main__":
    app = LabOpsTUI()
    app.run()