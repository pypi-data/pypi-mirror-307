from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal, Type, TypeVar, Union

import pyarrow as pa

from chalk.features.underscore import (
    Underscore,
    UnderscoreBinaryOp,
    UnderscoreBytesToString,
    UnderscoreCast,
    UnderscoreCoalesce,
    UnderscoreCosineSimilarity,
    UnderscoreFunction,
    UnderscoreGetJSONValue,
    UnderscoreGunzip,
    UnderscoreIfThenElse,
    UnderscoreMD5,
    UnderscoreSagemakerPredict,
    UnderscoreStringToBytes,
    UnderscoreTotalSeconds,
)

########################################################################################################################
# String Functions                                                                                                     #
########################################################################################################################


def replace(expr: Underscore | Any, old: str, new: str):
    """Replace all occurrences of a substring in a string with another substring.

    Parameters
    ----------
    expr
        The string to replace the substring in.
    old
        The substring to replace.
    new
        The substring to replace the old substring with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalized_name: str = F.replace(_.name, " ", "_")
    """
    return UnderscoreFunction("replace", expr, old, new)


def like(expr: Underscore | Any, pattern: str):
    """
    Evaluates if the string matches the pattern.

    Patterns can contain regular characters as well as wildcards.
    Wildcard characters can be escaped using the single character
    specified for the escape parameter. Matching is case-sensitive.

    Note: The wildcard `%` represents 0, 1 or multiple characters
    and the wildcard `_` represents exactly one character.

    For example, the pattern `John%` will match any string that starts
    with `John`, such as `John`, `JohnDoe`, `JohnSmith`, etc.

    The pattern `John_` will match any string that starts with `John`
    and is followed by exactly one character, such as `JohnD`, `JohnS`, etc.
    but not `John`, `JohnDoe`, `JohnSmith`, etc.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The pattern to check the string against.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    is_john: bool = F.like(_.name, "John%")
    """
    return UnderscoreFunction("like", expr, pattern)


def regexp_like(expr: Underscore | Any, pattern: str):
    """
    Evaluates the regular expression pattern and determines if it is contained within string.

    This function is similar to the `like` function, except that the pattern only needs to be
    contained within string, rather than needing to match all the string.
    In other words, this performs a contains operation rather than a match operation.
    You can match the entire string by anchoring the pattern using `^` and `$`.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    is_john: bool = F.regexp_like(_.name, "^John.*$")
    """
    return UnderscoreFunction("regexp_like", expr, pattern)


def regexp_extract(expr: Underscore | Any, pattern: str, group: int):
    """
    Finds the first occurrence of the regular expression pattern in the string and
    returns the capturing group number group.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.
    group
        The number of the capturing group to extract from the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class HiddenNumber:
    ...    id: str
    ...    hidden_number: str = "O0OOO",
    ...    number: str = F.regexp_extract(_.time,  r"([0-9]+)", 1)
    """
    return UnderscoreFunction("regexp_extract", expr, pattern, group)


def regexp_extract_all(expr: Underscore | Any, pattern: str, group: int):
    """
    Finds all occurrences of the regular expression pattern in string and
    returns the capturing group number group.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.
    group
        The number of the capturing group to extract from the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Time:
    ...    id: str
    ...    time: str = "1y 342d 20h 60m 6s",
    ...    processed_time: list[str] = F.regexp_extract_all(_.time, "([0-9]+)([ydhms])", 2)
    """
    return UnderscoreFunction("regexp_extract_all", expr, pattern, group)


def trim(expr: Underscore | Any):
    """
    Remove leading and trailing whitespace from a string.

    Parameters
    ----------
    expr
        The string to trim.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    trimmed_name: str = F.trim(_.name)
    """
    return UnderscoreFunction("trim", expr)


def starts_with(expr: Underscore | Any, prefix: Underscore | Any):
    """
    Evaluates if the string starts with the specified prefix.

    Parameters
    ----------
    expr
        The string to check against the prefix.
    prefix
        The prefix or feature to check if the string starts with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    is_food: bool = F.starts_with(_.name, "Food")
    """
    return UnderscoreFunction("starts_with", expr, prefix)


def ends_with(expr: Underscore | Any, suffix: Underscore | Any):
    """
    Evaluates if the string ends with the specified suffix.

    Parameters
    ----------
    expr
        The string to check against the suffix.
    suffix
        The suffix or feature to check if the string ends with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    is_food: bool = F.ends_with(_.name, "Food")
    """
    return UnderscoreFunction("ends_with", expr, suffix)


def substr(expr: Underscore, start: int, length: int | None = None):
    """
    Extract a substring from a string.

    Parameters
    ----------
    expr
        The string to extract the substring from.
    start
        The starting index of the substring (0-indexed).
    length
        The length of the substring. If None, the substring will extend to the end of the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    cat_first_three: str = F.substr(_.category, 0, 3)
    """
    if length is None:
        return UnderscoreFunction("substr", expr, start + 1)
    return UnderscoreFunction("substr", expr, start + 1, length)


def reverse(expr: Underscore | Any):
    """
    Reverse the order of a string.

    Parameters
    ----------
    expr
        The string to reverse.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    reversed_name: str = F.reverse(_.name)
    """
    return UnderscoreFunction("reverse", expr)


def levenshtein_distance(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Levenshtein distance between two strings.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.levenshtein_distance(_.name, _.email)
    """
    return UnderscoreFunction("levenshtein_distance", a, b)


def lower(expr: Underscore | Any):
    """
    Convert a string to lowercase.

    Parameters
    ----------
    expr
        The string to convert to lowercase.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalized: str = F.trim(F.lower(_.name))
    """
    return UnderscoreFunction("lower", expr)


def upper(expr: Underscore | Any):
    """
    Convert a string to uppercase.

    Parameters
    ----------
    expr
        The string to convert to uppercase.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    normalized: str = F.trim(F.upper(_.category))
    """
    return UnderscoreFunction("upper", expr)


def string_to_bytes(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert a string to bytes using the specified encoding.

    Parameters
    ----------
    expr
        An underscore expression for a feature to a
        string feature that should be converted to bytes.
    encoding
        The encoding to use when converting the string to bytes.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    hashed_name: bytes = F.string_to_bytes(_.name, encoding="utf-8")
    """
    return UnderscoreStringToBytes(expr, encoding)


def bytes_to_string(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert bytes to a string using the specified encoding.

    Parameters
    ----------
    expr
        A bytes feature to convert to a string.
    encoding
        The encoding to use when converting the bytes to a string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    hashed_name: bytes
    ...    decoded_name: str = F.bytes_to_string(_.hashed_name, encoding="utf-8")
    """
    return UnderscoreBytesToString(expr, encoding)


def split_part(expr: Any, delimiter: str, index: int):
    """
    Splits string by delimiter and returns the index'th element (0-indexed).
    If the index is larger than the number of fields, returns None.

    Parameters
    ----------
    expr:
        The string to split.
    delimiter:
        The delimiter to split the string on.
    index:
        The index of the the split to return.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CSVRow:
    ...    id: str
    ...    data: str
    ...    first_element: str = F.split_part(_.data, delimiter=",", index=0)
    """
    return UnderscoreFunction("split_part", expr, delimiter, index + 1)


########################################################################################################################
# URLs                                                                                                                 #
########################################################################################################################


def url_extract_protocol(expr: Any):
    """
    Extract the protocol from a URL.

    For example, the protocol of `https://www.google.com/cats` is `https`.

    Parameters
    ----------
    expr
        The URL to extract the protocol from.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     protocol: str = F.url_extract_protocol(_.website)
    """
    return UnderscoreFunction("url_extract_protocol", expr)


def url_extract_host(expr: Any):
    """
    Extract the host from a URL.

    For example, the host of `https://www.google.com/cats` is `www.google.com`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     host: str = F.url_extract_host(_.website)
    """
    return UnderscoreFunction("url_extract_host", expr)


def url_extract_path(expr: Any):
    """Extract the path from a URL.

    For example, the host of `https://www.google.com/cats` is `/cats`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     path: str = F.url_extract_path(_.website)
    """
    return UnderscoreFunction("url_extract_path", expr)


########################################################################################################################
# Misc                                                                                                                 #
########################################################################################################################


def md5(expr: Any):
    """
    Compute the MD5 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    md5_bytes: bytes = F.md5(_.bytes_feature)
    """
    return UnderscoreMD5(expr)


def coalesce(*vals: Any):
    """
    Return the first non-null entry

    Parameters
    ----------
    vals
        Expressions to coalesce. They can be a combination of underscores and literals,
        though types must be compatible (ie do not coalesce int and string).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    nickname: str | None
    ...    name: str | None
    ...    name_or_nickname: str = F.coalesce(_.name, _.nickname, "")
    """
    return UnderscoreCoalesce(*vals)


def is_null(expr: Any):
    """
    Check if a value is null.

    Parameters
    ----------
    expr
        The value to check if it is null.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    nickname: str | None
    ...    missing_nickname: bool = F.is_null(_.nickname)
    """
    return UnderscoreFunction("is_null", expr)


def if_then_else(condition: Underscore, if_true: Any, if_false: Any) -> Underscore:
    """
    Create a conditional expression, roughly equivalent to

    ```
    if condition:
        return if_true
    else:
        return if_false
    ```

    Unlike a Python if/else, all three inputs `(condition, if_true, if_false)` are evaluated
    in parallel for all rows, and then the correct side is selected based on the result of
    the condition expression.

    Examples
    --------
    >>> from chalk import _
    >>> from chalk.features import features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    amount: int
    ...    risk_score: bool = _.if_then_else(
    ...        _.amount > 10_000,
    ...        _.amount * 0.1,
    ...        _.amount * 0.05,
    ...    )
    """
    return UnderscoreIfThenElse(
        condition=condition,
        if_true=if_true,
        if_false=if_false,
    )


KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


def map_dict(
    d: dict[KeyType, ValueType],
    key: Underscore,
    *,
    default: ValueType | None,
):
    """
    Map a key to a value in a dictionary.

    Parameters
    ----------
    d
        The dictionary to map the key to a value in.
    key
        The key to look up in the dictionary.
    default
        The default value to return if the key is not found in the dictionary.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    merchant: str
    ...    merchant_risk_score: float = F.map_dict(
    ...        {"Amazon": 0.1, "Walmart": 0.08},
    ...        _.merchant,
    ...        default=0.,
    ...    )
    """
    result = default
    for k, value in d.items():
        result = if_then_else(key == k, value, result)
    return result


def sagemaker_predict(
    body: Underscore | Any,
    *,
    endpoint: str,
    content_type: str | None = None,
    target_model: str | None = None,
    target_variant: str | None = None,
    aws_access_key_id_override: str | None = None,
    aws_secret_access_key_override: str | None = None,
    aws_session_token_override: str | None = None,
    aws_region_override: str | None = None,
    aws_profile_name_override: str | None = None,
):
    """
    Runs a sagemaker prediction on the specified endpoint, passing in the serialized bytes as a feature.

    Parameters
    ----------
    body
        Bytes feature to be passed as the serialized input to the sagemaker endpoint.
    endpoint
        The name of the sagemaker endpoint.
    content_type
        The content type of the input data. If not specified, the content type will be inferred from the endpoint.
    target_model
        An optional argument which specifies the target model for the prediction.
        This should only be used for multimodel sagemaker endpoints.
    target_variant
        An optional argument which specifies the target variant for the prediction.
        This should only be used for multi variant sagemaker endpoints.
    aws_access_key_id_override
        An optional argument which specifies the AWS access key ID to use for the prediction.
    aws_secret_access_key_override
        An optional argument which specifies the AWS secret access key to use for the prediction.
    aws_session_token_override
        An optional argument which specifies the AWS session token to use for the prediction.
    aws_region_override
        An optional argument which specifies the AWS region to use for the prediction.
    aws_profile_name_override
        An optional argument which specifies the AWS profile name to use for the prediction

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    encoded_sagemaker_data: bytes
    ...    prediction: float = F.sagemaker_predict(
    ...        _.encoded_sagemaker_data,
    ...        endpoint="prediction-model_1.0.1_2024-09-16",
    ...        target_model="model_v2.tar.gz",
    ...        target_variant="blue"
    ...    )
    """
    return UnderscoreSagemakerPredict(
        body,
        endpoint=endpoint,
        content_type=content_type,
        target_model=target_model,
        target_variant=target_variant,
        aws_access_key_id_override=aws_access_key_id_override,
        aws_secret_access_key_override=aws_secret_access_key_override,
        aws_session_token_override=aws_session_token_override,
        aws_region_override=aws_region_override,
        aws_profile_name_override=aws_profile_name_override,
    )


def json_value(expr: Underscore, path: Union[str, Underscore]):
    """
    Extract a scalar from a JSON feature using a JSONPath expression. The value of the referenced path must be a JSON
    scalar (boolean, number, string).

    Parameters
    ----------
    expr
        The JSON feature to query.
    path
        The JSONPath-like expression to extract the scalar from the JSON feature.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk import JSON
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    profile: JSON
    ...    favorite_color: str = F.json_value(_.raw, "$.prefs.color")
    """

    return UnderscoreGetJSONValue(expr, path)


def gunzip(expr: Underscore):
    """
    Decompress a GZIP-compressed bytes feature.

    Parameters
    ----------
    expr
        The GZIP-compressed bytes feature to decompress.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    compressed_data: bytes
    ...    decompressed_data: bytes = F.gunzip(_.compressed_data)
    """
    return UnderscoreGunzip(expr)


def cosine_similarity(a: Underscore, b: Underscore):
    """
    Compute the cosine similarity between two vectors.

    Parameters
    ----------
    a
        The first vector.
    b
        The second vector.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    embedding: Vector[1536]
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    embedding: Vector[1536]
    >>> @features
    ... class UserMerchant:
    ...    id: str
    ...    user_id: User.id
    ...    user: User
    ...    merchant_id: Merchant.id
    ...    merchant: Merchant
    ...    similarity: float = F.cosine_similarity(_.user.embedding, _.merchant.embedding)
    """
    return UnderscoreCosineSimilarity(a, b)


########################################################################################################################
# Mathematical Functions                                                                                               #
########################################################################################################################


def power(a: Underscore | Any, b: Underscore | Any):
    """
    Raise a to the power of b. Alias for `a ** b`.

    Parameters
    ----------
    a
        The base.
    b
        The exponent.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    amount_std: float
    ...    amount_var: float = F.power(_.amount_std, 2)
    """
    return UnderscoreFunction("power", a, b)


def sqrt(expr: Underscore | Any):
    """
    Compute the square root of a number.

    Parameters
    ----------
    expr
        The number to compute the square root of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    amount_var: float
    ...    amount_std: float = F.sqrt(_.amount_var)
    """
    return UnderscoreFunction("sqrt", expr)


def sin(expr: Underscore | Any):
    """
    Compute the sine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    angle: float
    ...    sin_angle: float = F.sin(_.angle)
    """
    return UnderscoreFunction("sin", expr)


def asin(expr: Underscore | Any):
    """
    Compute the arcsine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    sin_angle: float
    ...    angle: float = F.asin(_.sin_angle)
    """
    return UnderscoreFunction("asin", expr)


def cos(expr: Underscore | Any):
    """
    Compute the cosine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    angle: float
    ...    cos_angle: float = F.cos(_.angle)
    """
    return UnderscoreFunction("cos", expr)


def acos(expr: Underscore | Any):
    """
    Compute the arccosine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    cos_angle: float
    ...    angle: float = F.acos(_.cos_angle)
    """
    return UnderscoreFunction("acos", expr)


def ln(expr: Underscore | Any):
    """
    Compute the natural logarithm of a number.

    Parameters
    ----------
    expr
        The number to compute the natural logarithm of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    hypotenuse: float
    ...    log_hypotenuse: float = F.ln(_.hypotenuse)
    """
    return UnderscoreFunction("ln", expr)


def exp(expr: Underscore | Any):
    """
    Returns Euler’s number raised to the power of x.

    Parameters
    ----------
    expr
        The exponent to raise Euler's number to.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    x: float
    ...    e_to_x: float = F.exp(_.x)
    """
    return UnderscoreFunction("exp", expr)


def sigmoid(x: Underscore | Any):
    """
    Compute the sigmoid of a number.

    Parameters
    ----------
    expr
        The number to compute the sigmoid of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Sigmoid:
    ...    id: str
    ...    x: float
    ...    sigmoid_of_x: float = F.sigmoid(_.x)
    """
    return UnderscoreBinaryOp(
        "/", 1, UnderscoreBinaryOp("+", 1, UnderscoreFunction("exp", UnderscoreBinaryOp("*", -1, x)))
    )


########################################################################################################################
# Date and Time Functions                                                                                              #
########################################################################################################################


def total_seconds(delta: Underscore) -> Underscore:
    """
    Compute the total number of seconds covered in a duration.

    Parameters
    ----------
    delta
        The duration to convert to seconds.

    Examples
    --------
    >>> from datetime import date
    >>> from chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    signup: date
    ...    last_login: date
    ...    signup_to_last_login_days: float = F.total_seconds(_.las_login - _.signup) / (60 * 60 * 24)
    """
    return UnderscoreTotalSeconds(delta)


def unix_seconds(expr: Underscore | Any):
    """
    Extract the number of seconds since the Unix epoch.
    Returned as a float.

    Parameters
    ----------
    expr
        The datetime to extract the number of seconds since the Unix epoch from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    unix_seconds: float = F.unix_seconds(_.date)
    """
    return UnderscoreFunction("to_unixtime", expr)


def unix_milliseconds(expr: Underscore | Any):
    """
    Extract the number of milliseconds since the Unix epoch.
    Returned as a float.

    Parameters
    ----------
    expr
        The datetime to extract the number of milliseconds since the Unix epoch from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    unix_milliseconds: float = F.unix_milliseconds(_.date)
    """
    return UnderscoreFunction("to_unixtime", expr) * 1000.0


def day_of_month(expr: Underscore | Any):
    """
    Extract the day of the month from a date.

    The supported types for x are date and datetime.

    Ranges from 1 to 31 inclusive.

    Parameters
    ----------
    expr
        The date to extract the day of the month from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_month(_.date)
    """
    return UnderscoreFunction("day_of_month", expr)


def day_of_week(expr: Underscore | Any):
    """
    Returns the ISO day of the week from x. The value ranges from 1 (Monday) to 7 (Sunday).

    Parameters
    ----------
    expr
        The date to extract the day of the week from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_week(_.date)
    """
    return UnderscoreFunction("day_of_week", expr)


def day_of_year(expr: Underscore | Any):
    """
    Extract the day of the year from a date.

    The value ranges from 1 to 366.

    Parameters
    ----------
    expr
        The date to extract the day of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_year(_.date)
    """
    return UnderscoreFunction("day_of_year", expr)


def month_of_year(expr: Underscore | Any):
    """
    Extract the month of the year from a date.

    The value ranges from 1 to 12.

    Parameters
    ----------
    expr
        The date to extract the month of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    month: int = F.month_of_year(_.date)
    """
    return UnderscoreFunction("month", expr)


def week_of_year(expr: Underscore | Any):
    """
    Extract the week of the year from a date.

    The value ranges from 1 to 53.

    Parameters
    ----------
    expr
        The date to extract the week of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    week: int = F.week_of_year(_.date)
    """
    return UnderscoreFunction("week_of_year", expr)


def hour_of_day(expr: Underscore | Any):
    """
    Extract the hour of the day from a datetime.

    The value ranges from 0 to 23.

    Parameters
    ----------
    expr
        The datetime to extract the hour of the day from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    hour: int = F.hour_of_day(_.date)
    """
    return UnderscoreFunction("hour", expr)


########################################################################################################################
# Array Functions                                                                                                      #
########################################################################################################################


def slice(arr: Underscore | list[Any], offset: Underscore | int, length: Underscore | int):
    """
    Returns a subset of the original array

    Parameters
    ----------
    arr
        The array to slice
    offset
        Starting index of the slice (0-indexed). If negative, slice starts from the end of the array
    length
        Length of the slice.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    three_most_recent_words: list[str] = F.slice(_.words, -3, 3) # computes ["zebra", "hello", "world"]
    """

    if isinstance(offset, int):
        start = offset if offset < 0 else offset + 1
    else:
        start = UnderscoreFunction(
            "if_else", UnderscoreBinaryOp("<", offset, 0), offset, UnderscoreBinaryOp("+", offset, 1)
        )
    return UnderscoreFunction("slice", arr, start, length)


########################################################################################################################
# Array functions                                                                                                      #
########################################################################################################################


def contains(
    arr: Underscore | list[Any],
    value: Any,
):
    """
    Returns whether the array contains the value.

    Parameters
    ----------
    arr
        The array to check for the value.
    value
        The value to check for in the array.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class APIRequest:
    ...    id: str
    ...    headers: list[str]
    ...    has_user_agent: bool = F.contains(_.headers, "User-Agent")
    """
    return UnderscoreFunction("contains", arr, value)


########################################################################################################################
# Additional Aggregations                                                                                              #
########################################################################################################################


def head(dataframe: Underscore | Any, n: Underscore | int):
    """
    Returns the first n items from a dataframe or has-many

    Parameters
    ----------
    dataframe
        the has-many from which the first n items are taken
    n
        how many items to take

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk import has_many, windowed, DataFrame, Windowed
    >>> from chalk.features import _, features, Primary
    >>> @features
    >>> class Merchant:
    ...     id: str
    ...
    >>> @features
    >>> class ConfirmedFraud:
    ...     id: int
    ...     trn_dt: datetime
    ...     is_fraud: int
    ...     mer_id: Merchant.id
    ...
    >>> @features
    >>> class MerchantFraud:
    ...     mer_id: Primary[Merchant.id]
    ...     merchant: Merchant
    ...     confirmed_fraud: DataFrame[ConfirmedFraud] = dataframe(
    ...         lambda: ConfirmedFraud.mer_id == MerchantFraud.mer_id,
    ...     )
    ...     first_five_merchant_window_fraud: Windowed[list[int]] = windowed(
    ...         "1d",
    ...         "30d",
    ...         expression=F.head(_.confirmed_fraud[_.trn_dt > _.chalk_window, _.id, _.is_fraud == 1], 5)
    ...     )
    """
    return slice(UnderscoreFunction("array_agg", dataframe), 0, n)


def haversine(
    lat1: Underscore | Any,
    lon1: Underscore | Any,
    lat2: Underscore | Any,
    lon2: Underscore | Any,
):
    """
    Compute the haversine distance (in kilometers) between two points on the Earth.

    Parameters
    ----------
    lat1
        The latitude of the first point.
    lon1
        The longitude of the first point.
    lat2
        The latitude of the second point.
    lon2
        The longitude of the second point.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Location:
    ...    id: str
    ...    lat1: float
    ...    lon1: float
    ...    lat2: float
    ...    lon2: float
    ...    distance: float = F.haversine(_.lat1, _.lon1, _.lat2, _.lon2)
    """
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = power(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * power(sin(dlon / 2), 2)
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return c * r


def cast(
    expr: Any,
    dtype: pa.DataType | Type[str] | Type[int] | Type[float] | Type[bool] | Type[datetime] | Type[date],
):
    """
    Cast an expression to a different type.

    Parameters
    ----------
    expr
        The expression to cast.
    dtype
        The type to cast the expression to.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    user_id: "User.id"
    ...    merchant_id: "Merchant.id"
    ...    user_merchant_id: "UserMerchant.id" = (
    ...        F.cast(_.user_id, str) + "_" +
    ...        F.cast(_.merchant_id, str)
    ...    )
    """
    if isinstance(dtype, type):
        if dtype is str:
            dtype = pa.string()
        elif dtype is int:
            dtype = pa.int64()
        elif dtype is float:
            dtype = pa.float64()
        elif dtype is bool:
            dtype = pa.bool_()
        elif dtype == datetime:
            dtype = pa.timestamp("us", "UTC")
        elif dtype == date:
            dtype = pa.date32()
    return UnderscoreCast(expr, dtype)


__all__ = (
    "acos",
    "asin",
    "bytes_to_string",
    "cast",
    "coalesce",
    "contains",
    "cos",
    "cosine_similarity",
    "day_of_month",
    "day_of_week",
    "day_of_year",
    "ends_with",
    "exp",
    "gunzip",
    "haversine",
    "head",
    "hour_of_day",
    "if_then_else",
    "is_null",
    "json_value",
    "levenshtein_distance",
    "like",
    "ln",
    "lower",
    "map_dict",
    "md5",
    "month_of_year",
    "power",
    "regexp_extract",
    "regexp_extract_all",
    "regexp_like",
    "replace",
    "reverse",
    "sagemaker_predict",
    "sigmoid",
    "sin",
    "slice",
    "split_part",
    "sqrt",
    "starts_with",
    "string_to_bytes",
    "substr",
    "total_seconds",
    "trim",
    "unix_milliseconds",
    "unix_seconds",
    "upper",
    "url_extract_host",
    "url_extract_path",
    "url_extract_protocol",
    "week_of_year",
)
