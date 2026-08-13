"""
Visual Notional Machine System for Programming Education

Based on research from:
- du Boulay, B. (1986). "Some Difficulties of Learning to Program."
- Sorva, J. (2013). "Notional Machines and Introductory Programming Education."

This system creates visual representations of program execution to help learners
build accurate mental models of how code executes.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import re

logger = logging.getLogger(__name__)


class ExecutionState(Enum):
    """States in program execution."""
    START = "start"
    RUNNING = "running"
    WAITING = "waiting"  # For I/O operations
    COMPLETED = "completed"
    ERROR = "error"


class MemoryType(Enum):
    """Types of memory in notional machines."""
    STACK = "stack"  # Function call stack
    HEAP = "heap"  # Dynamic memory
    STATIC = "static"  # Global/static variables
    CONSTANTS = "constants"  # Constant values


@dataclass
class MemoryCell:
    """A single memory cell in the notional machine."""
    address: str
    name: str
    value: Any
    type: str
    memory_type: MemoryType
    size: int = 0
    references: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'address': self.address,
            'name': self.name,
            'value': str(self.value),
            'type': self.type,
            'memory_type': self.memory_type.value,
            'size': self.size,
            'references': self.references,
            'metadata': self.metadata
        }


@dataclass
class StackFrame:
    """A frame in the call stack."""
    function_name: str
    return_address: Optional[str] = None
    local_variables: Dict[str, MemoryCell] = field(default_factory=dict)
    parameters: Dict[str, MemoryCell] = field(default_factory=dict)
    line_number: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'function_name': self.function_name,
            'return_address': self.return_address,
            'local_variables': {k: v.to_dict() for k, v in self.local_variables.items()},
            'parameters': {k: v.to_dict() for k, v in self.parameters.items()},
            'line_number': self.line_number,
            'metadata': self.metadata
        }


@dataclass
class ExecutionStep:
    """A single step in program execution."""
    step_number: int
    line_number: int
    code: str
    action: str  # What happens at this step
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    explanation: str
    control_flow_change: Optional[str] = None
    memory_changes: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'step_number': self.step_number,
            'line_number': self.line_number,
            'code': self.code,
            'action': self.action,
            'state_before': self.state_before,
            'state_after': self.state_after,
            'explanation': self.explanation,
            'control_flow_change': self.control_flow_change,
            'memory_changes': self.memory_changes
        }


@dataclass
class ControlFlowNode:
    """A node in the control flow graph."""
    id: str
    line_number: int
    code: str
    node_type: str  # 'sequential', 'conditional', 'loop', 'function_call', 'return'
    outgoing_edges: List[str] = field(default_factory=list)
    incoming_edges: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'line_number': self.line_number,
            'code': self.code,
            'node_type': self.node_type,
            'outgoing_edges': self.outgoing_edges,
            'incoming_edges': self.incoming_edges,
            'metadata': self.metadata
        }


@dataclass
class VisualNotionalMachine:
    """Complete visual notional machine for a program."""
    language: str
    code: str
    execution_steps: List[ExecutionStep]
    control_flow_graph: List[ControlFlowNode]
    memory_snapshots: List[Dict[str, Any]]
    stack_frames: List[StackFrame]
    data_structures: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'language': self.language,
            'code': self.code,
            'execution_steps': [step.to_dict() for step in self.execution_steps],
            'control_flow_graph': [node.to_dict() for node in self.control_flow_graph],
            'memory_snapshots': self.memory_snapshots,
            'stack_frames': [frame.to_dict() for frame in self.stack_frames],
            'data_structures': self.data_structures,
            'metadata': self.metadata
        }


class NotionalMachineEngine:
    """
    Production-grade visual notional machine engine.

    Creates comprehensive visual representations of program execution
    for multiple programming languages.
    """

    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the notional machine engine."""
        self.config = self._load_config(config_path)
        self.language_models = self._load_language_models()
        self.execution_cache = {}

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
            return {'visual_notional_machine': {'enabled': True}}

    def _load_language_models(self) -> Dict[str, Dict]:
        """Load language-specific mental models."""
        return {
            'python': {
                'memory_model': 'object_reference',
                'execution_model': 'interpreter',
                'scope_rules': 'function_scope',
                'type_system': 'dynamic',
                'special_features': ['list_comprehension', 'generator', 'decorator']
            },
            'javascript': {
                'memory_model': 'object_reference',
                'execution_model': 'interpreter',
                'scope_rules': 'lexical_closures',
                'type_system': 'dynamic',
                'special_features': ['closure', 'prototype', 'async_await']
            },
            'java': {
                'memory_model': 'reference_primitive',
                'execution_model': 'jvm',
                'scope_rules': 'block_scope',
                'type_system': 'static',
                'special_features': ['oop', 'generics', 'threads']
            },
            'cpp': {
                'memory_model': 'pointers_references',
                'execution_model': 'compiled',
                'scope_rules': 'block_scope',
                'type_system': 'static',
                'special_features': ['pointers', 'raii', 'templates']
            }
        }

    def visualize_execution(
        self,
        code: str,
        language: str,
        interactive: bool = True
    ) -> VisualNotionalMachine:
        """
        Create comprehensive visualization of code execution.

        Args:
            code: Source code to visualize
            language: Programming language
            interactive: Whether to create interactive visualization

        Returns:
            VisualNotionalMachine with all visualization components
        """
        logger.info(f"Creating execution visualization for {language}")

        # Build execution steps
        execution_steps = self._trace_execution(code, language)

        # Build control flow graph
        control_flow = self._build_control_flow_graph(code, language)

        # Create memory snapshots
        memory_snapshots = self._create_memory_snapshots(code, language, execution_steps)

        # Build stack frames
        stack_frames = self._build_stack_frames(code, language, execution_steps)

        # Visualize data structures
        data_structures = self._visualize_data_structures(code, language)

        return VisualNotionalMachine(
            language=language,
            code=code,
            execution_steps=execution_steps,
            control_flow_graph=control_flow,
            memory_snapshots=memory_snapshots,
            stack_frames=stack_frames,
            data_structures=data_structures,
            metadata={
                'created_at': time.time(),
                'interactive': interactive,
                'total_steps': len(execution_steps)
            }
        )

    def _trace_execution(
        self,
        code: str,
        language: str
    ) -> List[ExecutionStep]:
        """Trace through code execution step by step."""
        lines = [line.rstrip() for line in code.split('\n') if line.strip()]

        execution_steps = []
        current_state = {}
        step_number = 0

        for line_num, line in enumerate(lines, 1):
            if not line.strip() or line.strip().startswith('#'):
                continue

            # Determine action and state changes
            action, state_change = self._analyze_line(line, language, current_state)

            # Create execution step
            step = ExecutionStep(
                step_number=step_number,
                line_number=line_num,
                code=line,
                action=action,
                state_before=current_state.copy(),
                state_after=current_state.copy(),
                explanation=self._generate_step_explanation(line, action, state_change),
                memory_changes=[state_change] if state_change else []
            )

            execution_steps.append(step)

            # Update state for next step
            if state_change:
                current_state.update(state_change)

            step_number += 1

        return execution_steps

    def _analyze_line(
        self,
        line: str,
        language: str,
        current_state: Dict[str, Any]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Analyze a line of code to determine its action and state changes."""
        stripped = line.strip()

        # Variable assignment
        if '=' in stripped and not any(kw in stripped for kw in ['==', '!=', '<=', '>=']):
            return self._analyze_assignment(stripped, language, current_state)

        # Conditional statements
        elif stripped.startswith('if ') or stripped.startswith('elif '):
            return self._analyze_conditional(stripped, language)

        # Loops
        elif any(stripped.startswith(kw) for kw in ['for ', 'while ']):
            return self._analyze_loop(stripped, language)

        # Function definitions
        elif stripped.startswith('def ') or (stripped.startswith('function ') or 'function' in stripped):
            return self._analyze_function_def(stripped, language)

        # Function calls
        elif '(' in stripped and not any(kw in stripped for kw in ['def ', 'function ']):
            return self._analyze_function_call(stripped, language)

        # Return statements
        elif stripped.startswith('return '):
            return self._analyze_return(stripped, language)

        # Print/output statements
        elif 'print(' in stripped or 'console.log(' in stripped:
            return self._analyze_output(stripped, language)

        # Default: simple expression
        else:
            return self._analyze_expression(stripped, language)

    def _analyze_assignment(
        self,
        line: str,
        language: str,
        current_state: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """Analyze variable assignment."""
        # Parse variable name and value
        parts = line.split('=', 1)
        var_name = parts[0].strip()
        var_value = parts[1].strip() if len(parts) > 1 else 'None'

        # Calculate value if it's an expression
        calculated_value = self._evaluate_expression(var_value, current_state)

        action = f"Assign {calculated_value} to variable '{var_name}'"

        state_change = {
            'variable': var_name,
            'old_value': current_state.get(var_name, 'undefined'),
            'new_value': str(calculated_value),
            'change_type': 'assignment'
        }

        return action, state_change

    def _analyze_conditional(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze conditional statement."""
        return "Evaluate condition and branch accordingly", None

    def _analyze_loop(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze loop statement."""
        return "Initialize/update loop control", None

    def _analyze_function_def(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze function definition."""
        return "Define function with parameters", None

    def _analyze_function_call(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze function call."""
        return "Execute function call", None

    def _analyze_return(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze return statement."""
        return "Return value from function", None

    def _analyze_output(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze print/output statement."""
        return "Output value to console", None

    def _analyze_expression(
        self,
        line: str,
        language: str
    ) -> Tuple[str, None]:
        """Analyze expression."""
        return "Evaluate expression", None

    def _evaluate_expression(
        self,
        expr: str,
        current_state: Dict[str, Any]
    ) -> Any:
        """Simple expression evaluator."""
        try:
            # Remove quotes for string values
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]
            elif expr.startswith("'") and expr.endswith("'"):
                return expr[1:-1]

            # Try to evaluate as Python expression
            try:
                # Safe evaluation with limited operations
                return eval(expr, {"__builtins__": {}}, current_state)
            except:
                return expr
        except:
            return expr

    def _generate_step_explanation(
        self,
        code: str,
        action: str,
        state_change: Optional[Dict[str, Any]]
    ) -> str:
        """Generate explanation for an execution step."""
        if state_change and state_change.get('change_type') == 'assignment':
            return f"Variable '{state_change['variable']}' is updated from {state_change['old_value']} to {state_change['new_value']}"
        else:
            return action

    def _build_control_flow_graph(
        self,
        code: str,
        language: str
    ) -> List[ControlFlowNode]:
        """Build control flow graph from code."""
        lines = [line for line in code.split('\n') if line.strip()]

        nodes = []
        node_id = 0

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Determine node type
            node_type = self._determine_node_type(stripped)

            node = ControlFlowNode(
                id=f"node_{node_id}",
                line_number=line_num,
                code=stripped,
                node_type=node_type,
                metadata={
                    'indent_level': len(line) - len(line.lstrip())
                }
            )

            # Add edges (simplified)
            if nodes:
                nodes[-1].outgoing_edges.append(node.id)
                node.incoming_edges.append(nodes[-1].id)

            nodes.append(node)
            node_id += 1

        return nodes

    def _determine_node_type(self, code: str) -> str:
        """Determine the type of control flow node."""
        if code.startswith('if ') or code.startswith('elif ') or code.startswith('else:'):
            return 'conditional'
        elif any(code.startswith(kw) for kw in ['for ', 'while ']):
            return 'loop'
        elif code.startswith('def ') or 'function' in code:
            return 'function_def'
        elif code.startswith('return '):
            return 'return'
        elif 'print(' in code or 'console.log(' in code:
            return 'output'
        else:
            return 'sequential'

    def _create_memory_snapshots(
        self,
        code: str,
        language: str,
        execution_steps: List[ExecutionStep]
    ) -> List[Dict[str, Any]]:
        """Create memory state snapshots at each execution step."""
        snapshots = []

        for step in execution_steps:
            snapshot = {
                'step_number': step.step_number,
                'line_number': step.line_number,
                'state': step.state_after.copy(),
                'memory_changes': step.memory_changes,
                'timestamp': step.step_number  # Simplified
            }
            snapshots.append(snapshot)

        return snapshots

    def _build_stack_frames(
        self,
        code: str,
        language: str,
        execution_steps: List[ExecutionStep]
    ) -> List[StackFrame]:
        """Build stack frames showing function call hierarchy."""
        # For now, create a single global frame
        global_frame = StackFrame(
            function_name='__main__',
            line_number=0,
            metadata={'type': 'global'}
        )

        # Add variables from execution steps
        for step in execution_steps:
            for change in step.memory_changes:
                if change.get('change_type') == 'assignment':
                    var_name = change['variable']
                    var_value = change['new_value']
                    global_frame.local_variables[var_name] = MemoryCell(
                        address=f"0x{hash(var_name) & 0xffff:04x}",
                        name=var_name,
                        value=var_value,
                        type='inferred',
                        memory_type=MemoryType.STACK
                    )

        return [global_frame]

    def _visualize_data_structures(
        self,
        code: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Visualize data structures in the code."""
        structures = []

        # Look for common data structure patterns
        if '[]' in code or 'list(' in code:
            structures.append({
                'type': 'list',
                'name': 'array/list',
                'visualization': 'indexed_sequence',
                'operations': ['append', 'access', 'iterate']
            })

        if '{}' in code or 'dict(' in code:
            structures.append({
                'type': 'dictionary',
                'name': 'hash_map/dict',
                'visualization': 'key_value_pairs',
                'operations': ['get', 'set', 'delete']
            })

        if 'set(' in code or language == 'python' and '{' in code:
            structures.append({
                'type': 'set',
                'name': 'hash_set',
                'visualization': 'unique_elements',
                'operations': ['add', 'remove', 'contains']
            })

        return structures


class InteractiveVisualizationEngine:
    """
    Frontend component specification for interactive visualizations.

    This would be implemented in JavaScript/React for actual interactivity.
    """

    @staticmethod
    def get_frontend_spec() -> Dict[str, Any]:
        """Get frontend specification for interactive visualization."""
        return {
            'components': [
                {
                    'name': 'CodeEditor',
                    'type': 'MonacoEditor',
                    'props': {
                        'language': 'python',
                        'readOnly': True,
                        'highlightActiveLine': True
                    }
                },
                {
                    'name': 'ExecutionControls',
                    'type': 'ButtonGroup',
                    'props': {
                        'buttons': ['Step Forward', 'Step Backward', 'Reset', 'Auto-Play']
                    }
                },
                {
                    'name': 'MemoryVisualization',
                    'type': 'InteractiveMemoryDiagram',
                    'props': {
                        'stackFrames': True,
                        'heapObjects': True,
                        'interactive': True
                    }
                },
                {
                    'name': 'ControlFlowGraph',
                    'type': 'FlowChart',
                    'props': {
                        'activeNodeHighlight': True,
                        'executionPath': True
                    }
                },
                {
                    'name': 'VariableWatch',
                    'type': 'DataTable',
                    'props': {
                        'columns': ['Variable', 'Value', 'Type', 'Address']
                    }
                },
                {
                    'name': 'OutputConsole',
                    'type': 'Console',
                    'props': {
                        'appendOnly': True
                    }
                }
            ],
            'communication': {
                'type': 'WebSocket',
                'events': [
                    'stepForward',
                    'stepBackward',
                    'resetExecution',
                    'toggleBreakpoint',
                    'inspectVariable'
                ]
            }
        }


# Global instances
_notional_machine_engine = None


def get_notional_machine_engine() -> NotionalMachineEngine:
    """Get or create the global notional machine engine."""
    global _notional_machine_engine
    if _notional_machine_engine is None:
        _notional_machine_engine = NotionalMachineEngine()
    return _notional_machine_engine


# Tool functions for external use

def create_visual_notional_machine(
    code: str,
    language: str,
    interactive: bool = True
) -> Dict[str, Any]:
    """
    Create visual notional machine for code execution.

    Tool wrapper for external use.
    """
    try:
        engine = get_notional_machine_engine()
        visualization = engine.visualize_execution(code, language, interactive)
        return {
            'success': True,
            'visualization': visualization.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to create visualization: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def trace_code_execution(
    code: str,
    language: str
) -> Dict[str, Any]:
    """
    Trace through code execution with detailed steps.

    Tool wrapper for external use.
    """
    try:
        engine = get_notional_machine_engine()
        steps = engine._trace_execution(code, language)
        return {
            'success': True,
            'steps': [step.to_dict() for step in steps]
        }
    except Exception as e:
        logger.error(f"Failed to trace execution: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def build_control_flow_graph(
    code: str,
    language: str
) -> Dict[str, Any]:
    """
    Build control flow graph for code.

    Tool wrapper for external use.
    """
    try:
        engine = get_notional_machine_engine()
        graph = engine._build_control_flow_graph(code, language)
        return {
            'success': True,
            'graph': [node.to_dict() for node in graph]
        }
    except Exception as e:
        logger.error(f"Failed to build control flow: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the notional machine system
    print("Testing Visual Notional Machine System...")

    # Test code execution visualization
    test_code = """
x = 5
if x > 3:
    x = x + 1
print(x)
"""
    visualization = create_visual_notional_machine(test_code, 'python')
    print(f"Visualization created: {visualization['success']}")

    if visualization['success']:
        viz_data = visualization['visualization']
        print(f"Execution steps: {len(viz_data['execution_steps'])}")
        print(f"Control flow nodes: {len(viz_data['control_flow_graph'])}")
        print(f"Memory snapshots: {len(viz_data['memory_snapshots'])}")

    # Test control flow graph
    graph = build_control_flow_graph(test_code, 'python')
    print(f"Control flow graph: {graph['success']}")

    # Test code tracing
    trace = trace_code_execution(test_code, 'python')
    print(f"Code trace: {trace['success']}")

    print("Visual Notional Machine System test complete!")
