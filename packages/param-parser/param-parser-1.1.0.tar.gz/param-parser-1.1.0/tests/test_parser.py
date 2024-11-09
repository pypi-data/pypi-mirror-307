import pytest

import param_parser


def test_empty():
    result = param_parser.parse("")

    assert len(result) == 0


def test_single_sequence_node():
    result = param_parser.parse(r"this/is/a/test")

    assert len(result) == 1

    assert isinstance(result[0], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/is/a/test"


def test_single_param_node():
    result = param_parser.parse(r"{this_is_a_test}")

    assert len(result) == 1

    assert isinstance(result[0], param_parser.ParamNode)

    assert result[0].param_name == "this_is_a_test"
    assert result[0].param_type == None
    assert result[0].param_options == []


def test_untyped_param_node_1():
    result = param_parser.parse(r"this/{is}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == "is"
    assert result[1].param_type == None
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_untyped_param_node_2():
    result = param_parser.parse(r"this/{is:}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == "is"
    assert result[1].param_type == None
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_1():
    result = param_parser.parse(r"this/{is:string}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == "is"
    assert result[1].param_type == "string"
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_2():
    result = param_parser.parse(r"this/{is:string:}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == "is"
    assert result[1].param_type == "string"
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_options_1():
    result = param_parser.parse(r"this/{is:string:1,2,3}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == "is"
    assert result[1].param_type == "string"
    assert result[1].param_options == ["1", "2", "3"]

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_options_2():
    result = param_parser.parse(r"this/{is:string:1,2,3,}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == "is"
    assert result[1].param_type == "string"
    assert result[1].param_options == ["1", "2", "3"]

    assert result[2].sequence_value == "/a/test"


def test_single_sequence_node_with_escaped_brackets():
    result = param_parser.parse(r"this/\{is:string:1,2,3\}/a/test")

    assert len(result) == 1

    assert isinstance(result[0], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/{is:string:1,2,3}/a/test"


def test_untyped_param_node_with_escaped_colon_1():
    result = param_parser.parse(r"this/{\:}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == ":"
    assert result[1].param_type == None
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_untyped_param_node_with_escaped_colon_2():
    result = param_parser.parse(r"this/{\::}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == ":"
    assert result[1].param_type == None
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_escaped_colon_1():
    result = param_parser.parse(r"this/{\::string\:}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == ":"
    assert result[1].param_type == "string:"
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_escaped_colon_2():
    result = param_parser.parse(r"this/{\::string\::}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == ":"
    assert result[1].param_type == "string:"
    assert result[1].param_options == []

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_options_and_escaped_comma_1():
    result = param_parser.parse(r"this/{\::string\::1\,2\,3\,}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == ":"
    assert result[1].param_type == "string:"
    assert result[1].param_options == ["1,2,3,"]

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_options_and_escaped_comma_2():
    result = param_parser.parse(r"this/{\::string\::1\,2\,3\,,}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/"

    assert result[1].param_name == ":"
    assert result[1].param_type == "string:"
    assert result[1].param_options == ["1,2,3,"]

    assert result[2].sequence_value == "/a/test"


def test_typed_param_node_with_options_and_escaped_backslash():
    result = param_parser.parse(r"this/\\{is\\:string\\:1,2,3\\}/a/test")

    assert len(result) == 3

    assert isinstance(result[0], param_parser.SequenceNode)
    assert isinstance(result[1], param_parser.ParamNode)
    assert isinstance(result[2], param_parser.SequenceNode)

    assert result[0].sequence_value == "this/\\"

    assert result[1].param_name == "is\\"
    assert result[1].param_type == "string\\"
    assert result[1].param_options == ["1", "2", "3\\"]

    assert result[2].sequence_value == "/a/test"


def test_multiple_untyped_param_nodes():
    result = param_parser.parse(r"{this}/{is}/{a}/{test}")

    assert len(result) == 7

    assert isinstance(result[0], param_parser.ParamNode)
    assert isinstance(result[1], param_parser.SequenceNode)
    assert isinstance(result[2], param_parser.ParamNode)
    assert isinstance(result[3], param_parser.SequenceNode)
    assert isinstance(result[4], param_parser.ParamNode)
    assert isinstance(result[5], param_parser.SequenceNode)
    assert isinstance(result[6], param_parser.ParamNode)

    assert result[0].param_name == "this"
    assert result[0].param_type == None
    assert result[0].param_options == []

    assert result[1].sequence_value == "/"

    assert result[2].param_name == "is"
    assert result[2].param_type == None
    assert result[2].param_options == []

    assert result[3].sequence_value == "/"

    assert result[4].param_name == "a"
    assert result[4].param_type == None
    assert result[4].param_options == []

    assert result[5].sequence_value == "/"

    assert result[6].param_name == "test"
    assert result[6].param_type == None
    assert result[6].param_options == []


def test_invalid_syntax_on_brackets_1():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/{is:string:1,2,3\}/a/test")

    assert str(exc_info.value) == "Unexpected token 'EOF' at position '30'"


def test_invalid_syntax_on_brackets_2():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/\{is:string:1,2,3}/a/test")

    assert str(exc_info.value) == "Unexpected token 'RC_BRACKET' at position '22'"


def test_invalid_syntax_on_brackets_3():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/{}/a/test")

    assert str(exc_info.value) == "Unexpected token 'RC_BRACKET' at position '6'"


def test_invalid_syntax_on_brackets_4():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"}this/is/a/test")

    assert str(exc_info.value) == "Unexpected token 'RC_BRACKET' at position '0'"


def test_invalid_syntax_on_colon_1():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/{is::}/a/test")

    assert str(exc_info.value) == "Unexpected token 'COLON' at position '9'"


def test_invalid_syntax_on_colon_2():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/{is:string:1,2,3:}/a/test")

    assert str(exc_info.value) == "Unexpected token 'COLON' at position '21'"


def test_invalid_syntax_on_comma_1():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/{is:string:,}/a/test")

    assert str(exc_info.value) == "Unexpected token 'COMMA' at position '16'"


def test_invalid_syntax_on_comma_2():
    with pytest.raises(param_parser.ParserSyntaxException) as exc_info:
        param_parser.parse(r"this/{is:string:1,2,3,,}/a/test")

    assert str(exc_info.value) == "Unexpected token 'COMMA' at position '22'"
