#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 55
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 34
#define ALIAS_COUNT 0
#define TOKEN_COUNT 16
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 9
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 10

enum ts_symbol_identifiers {
  anon_sym_DOT = 1,
  sym_NAME = 2,
  aux_sym_float_token1 = 3,
  sym__DIGITS = 4,
  sym__SIGN = 5,
  anon_sym_STAR = 6,
  anon_sym_SLASH = 7,
  anon_sym_CARET = 8,
  anon_sym_STAR_STAR = 9,
  aux_sym_unit_token1 = 10,
  anon_sym_u00b0 = 11,
  anon_sym_PERCENT = 12,
  anon_sym_LPAREN = 13,
  anon_sym_RPAREN = 14,
  anon_sym_COMMA = 15,
  sym_expression = 16,
  sym__sub_expression = 17,
  sym_variable = 18,
  sym__DOT = 19,
  sym__scalar = 20,
  sym__number = 21,
  sym_integer = 22,
  sym_float = 23,
  sym_quantity = 24,
  sym_units = 25,
  sym_unit_term = 26,
  sym_unit = 27,
  sym_call = 28,
  sym_args = 29,
  aux_sym_variable_repeat1 = 30,
  aux_sym_units_repeat1 = 31,
  aux_sym_units_repeat2 = 32,
  aux_sym_args_repeat1 = 33,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_DOT] = ".",
  [sym_NAME] = "NAME",
  [aux_sym_float_token1] = "float_token1",
  [sym__DIGITS] = "_DIGITS",
  [sym__SIGN] = "_SIGN",
  [anon_sym_STAR] = "*",
  [anon_sym_SLASH] = "/",
  [anon_sym_CARET] = "^",
  [anon_sym_STAR_STAR] = "**",
  [aux_sym_unit_token1] = "unit_token1",
  [anon_sym_u00b0] = "\u00b0",
  [anon_sym_PERCENT] = "%",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_COMMA] = ",",
  [sym_expression] = "expression",
  [sym__sub_expression] = "_sub_expression",
  [sym_variable] = "variable",
  [sym__DOT] = "_DOT",
  [sym__scalar] = "_scalar",
  [sym__number] = "_number",
  [sym_integer] = "integer",
  [sym_float] = "float",
  [sym_quantity] = "quantity",
  [sym_units] = "units",
  [sym_unit_term] = "unit_term",
  [sym_unit] = "unit",
  [sym_call] = "call",
  [sym_args] = "args",
  [aux_sym_variable_repeat1] = "variable_repeat1",
  [aux_sym_units_repeat1] = "units_repeat1",
  [aux_sym_units_repeat2] = "units_repeat2",
  [aux_sym_args_repeat1] = "args_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_DOT] = anon_sym_DOT,
  [sym_NAME] = sym_NAME,
  [aux_sym_float_token1] = aux_sym_float_token1,
  [sym__DIGITS] = sym__DIGITS,
  [sym__SIGN] = sym__SIGN,
  [anon_sym_STAR] = anon_sym_STAR,
  [anon_sym_SLASH] = anon_sym_SLASH,
  [anon_sym_CARET] = anon_sym_CARET,
  [anon_sym_STAR_STAR] = anon_sym_STAR_STAR,
  [aux_sym_unit_token1] = aux_sym_unit_token1,
  [anon_sym_u00b0] = anon_sym_u00b0,
  [anon_sym_PERCENT] = anon_sym_PERCENT,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [sym_expression] = sym_expression,
  [sym__sub_expression] = sym__sub_expression,
  [sym_variable] = sym_variable,
  [sym__DOT] = sym__DOT,
  [sym__scalar] = sym__scalar,
  [sym__number] = sym__number,
  [sym_integer] = sym_integer,
  [sym_float] = sym_float,
  [sym_quantity] = sym_quantity,
  [sym_units] = sym_units,
  [sym_unit_term] = sym_unit_term,
  [sym_unit] = sym_unit,
  [sym_call] = sym_call,
  [sym_args] = sym_args,
  [aux_sym_variable_repeat1] = aux_sym_variable_repeat1,
  [aux_sym_units_repeat1] = aux_sym_units_repeat1,
  [aux_sym_units_repeat2] = aux_sym_units_repeat2,
  [aux_sym_args_repeat1] = aux_sym_args_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_DOT] = {
    .visible = true,
    .named = false,
  },
  [sym_NAME] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_float_token1] = {
    .visible = false,
    .named = false,
  },
  [sym__DIGITS] = {
    .visible = false,
    .named = true,
  },
  [sym__SIGN] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_STAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SLASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CARET] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STAR_STAR] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_unit_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_u00b0] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PERCENT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [sym_expression] = {
    .visible = true,
    .named = true,
  },
  [sym__sub_expression] = {
    .visible = false,
    .named = true,
  },
  [sym_variable] = {
    .visible = true,
    .named = true,
  },
  [sym__DOT] = {
    .visible = false,
    .named = true,
  },
  [sym__scalar] = {
    .visible = false,
    .named = true,
  },
  [sym__number] = {
    .visible = false,
    .named = true,
  },
  [sym_integer] = {
    .visible = true,
    .named = true,
  },
  [sym_float] = {
    .visible = true,
    .named = true,
  },
  [sym_quantity] = {
    .visible = true,
    .named = true,
  },
  [sym_units] = {
    .visible = true,
    .named = true,
  },
  [sym_unit_term] = {
    .visible = true,
    .named = true,
  },
  [sym_unit] = {
    .visible = true,
    .named = true,
  },
  [sym_call] = {
    .visible = true,
    .named = true,
  },
  [sym_args] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_variable_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_units_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_units_repeat2] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_args_repeat1] = {
    .visible = false,
    .named = false,
  },
};

enum ts_field_identifiers {
  field_args = 1,
  field_divisive = 2,
  field_exponent = 3,
  field_first = 4,
  field_function = 5,
  field_magnitude = 6,
  field_multiplicative = 7,
  field_unit = 8,
  field_units = 9,
};

static const char * const ts_field_names[] = {
  [0] = NULL,
  [field_args] = "args",
  [field_divisive] = "divisive",
  [field_exponent] = "exponent",
  [field_first] = "first",
  [field_function] = "function",
  [field_magnitude] = "magnitude",
  [field_multiplicative] = "multiplicative",
  [field_unit] = "unit",
  [field_units] = "units",
};

static const TSFieldMapSlice ts_field_map_slices[PRODUCTION_ID_COUNT] = {
  [1] = {.index = 0, .length = 2},
  [2] = {.index = 2, .length = 1},
  [3] = {.index = 3, .length = 1},
  [4] = {.index = 4, .length = 1},
  [5] = {.index = 5, .length = 2},
  [6] = {.index = 7, .length = 2},
  [7] = {.index = 9, .length = 2},
  [8] = {.index = 11, .length = 3},
  [9] = {.index = 14, .length = 2},
};

static const TSFieldMapEntry ts_field_map_entries[] = {
  [0] =
    {field_magnitude, 0},
    {field_units, 1},
  [2] =
    {field_first, 0},
  [3] =
    {field_unit, 0},
  [4] =
    {field_function, 0},
  [5] =
    {field_first, 0},
    {field_multiplicative, 1},
  [7] =
    {field_divisive, 1},
    {field_first, 0},
  [9] =
    {field_args, 2},
    {field_function, 0},
  [11] =
    {field_divisive, 2},
    {field_first, 0},
    {field_multiplicative, 1},
  [14] =
    {field_exponent, 2},
    {field_unit, 0},
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 48,
  [49] = 49,
  [50] = 50,
  [51] = 51,
  [52] = 52,
  [53] = 53,
  [54] = 54,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(4);
      ADVANCE_MAP(
        '%', 20,
        '(', 21,
        ')', 22,
        '*', 14,
        ',', 23,
        '.', 5,
        '/', 15,
        '^', 16,
        0xb0, 19,
        '+', 13,
        '-', 13,
        'E', 6,
        'e', 6,
      );
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(0);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 1:
      if (lookahead == ')') ADVANCE(22);
      if (lookahead == '.') ADVANCE(5);
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(13);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(1);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(8);
      END_STATE();
    case 2:
      if (eof) ADVANCE(4);
      if (lookahead == '%') ADVANCE(20);
      if (lookahead == ')') ADVANCE(22);
      if (lookahead == '*') ADVANCE(14);
      if (lookahead == ',') ADVANCE(23);
      if (lookahead == '/') ADVANCE(15);
      if (lookahead == '^') ADVANCE(16);
      if (lookahead == 0xb0) ADVANCE(19);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(2);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(18);
      END_STATE();
    case 3:
      if (eof) ADVANCE(4);
      if (lookahead == '%') ADVANCE(20);
      if (lookahead == ')') ADVANCE(22);
      if (lookahead == ',') ADVANCE(23);
      if (lookahead == '.') ADVANCE(5);
      if (lookahead == 0xb0) ADVANCE(19);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(10);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(3);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(18);
      END_STATE();
    case 4:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 5:
      ACCEPT_TOKEN(anon_sym_DOT);
      END_STATE();
    case 6:
      ACCEPT_TOKEN(sym_NAME);
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(9);
      if (('0' <= lookahead && lookahead <= '9') ||
          lookahead == '_') ADVANCE(8);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 7:
      ACCEPT_TOKEN(sym_NAME);
      if (('0' <= lookahead && lookahead <= '9') ||
          lookahead == '_') ADVANCE(8);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 8:
      ACCEPT_TOKEN(sym_NAME);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(8);
      END_STATE();
    case 9:
      ACCEPT_TOKEN(aux_sym_float_token1);
      END_STATE();
    case 10:
      ACCEPT_TOKEN(aux_sym_float_token1);
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(9);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(18);
      END_STATE();
    case 11:
      ACCEPT_TOKEN(sym__DIGITS);
      if (lookahead == '_') ADVANCE(12);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      END_STATE();
    case 12:
      ACCEPT_TOKEN(sym__DIGITS);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      END_STATE();
    case 13:
      ACCEPT_TOKEN(sym__SIGN);
      END_STATE();
    case 14:
      ACCEPT_TOKEN(anon_sym_STAR);
      if (lookahead == '*') ADVANCE(17);
      END_STATE();
    case 15:
      ACCEPT_TOKEN(anon_sym_SLASH);
      END_STATE();
    case 16:
      ACCEPT_TOKEN(anon_sym_CARET);
      END_STATE();
    case 17:
      ACCEPT_TOKEN(anon_sym_STAR_STAR);
      END_STATE();
    case 18:
      ACCEPT_TOKEN(aux_sym_unit_token1);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(18);
      END_STATE();
    case 19:
      ACCEPT_TOKEN(anon_sym_u00b0);
      END_STATE();
    case 20:
      ACCEPT_TOKEN(anon_sym_PERCENT);
      END_STATE();
    case 21:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 22:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 23:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 1},
  [2] = {.lex_state = 1},
  [3] = {.lex_state = 2},
  [4] = {.lex_state = 1},
  [5] = {.lex_state = 2},
  [6] = {.lex_state = 2},
  [7] = {.lex_state = 2},
  [8] = {.lex_state = 2},
  [9] = {.lex_state = 2},
  [10] = {.lex_state = 2},
  [11] = {.lex_state = 3},
  [12] = {.lex_state = 3},
  [13] = {.lex_state = 3},
  [14] = {.lex_state = 3},
  [15] = {.lex_state = 2},
  [16] = {.lex_state = 2},
  [17] = {.lex_state = 2},
  [18] = {.lex_state = 0},
  [19] = {.lex_state = 3},
  [20] = {.lex_state = 3},
  [21] = {.lex_state = 3},
  [22] = {.lex_state = 2},
  [23] = {.lex_state = 0},
  [24] = {.lex_state = 2},
  [25] = {.lex_state = 2},
  [26] = {.lex_state = 0},
  [27] = {.lex_state = 2},
  [28] = {.lex_state = 2},
  [29] = {.lex_state = 2},
  [30] = {.lex_state = 0},
  [31] = {.lex_state = 0},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 0},
  [35] = {.lex_state = 0},
  [36] = {.lex_state = 0},
  [37] = {.lex_state = 0},
  [38] = {.lex_state = 0},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 0},
  [41] = {.lex_state = 0},
  [42] = {.lex_state = 0},
  [43] = {.lex_state = 0},
  [44] = {.lex_state = 0},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 0},
  [47] = {.lex_state = 0},
  [48] = {.lex_state = 0},
  [49] = {.lex_state = 0},
  [50] = {.lex_state = 0},
  [51] = {.lex_state = 0},
  [52] = {.lex_state = 0},
  [53] = {.lex_state = 1},
  [54] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_DOT] = ACTIONS(1),
    [sym_NAME] = ACTIONS(1),
    [aux_sym_float_token1] = ACTIONS(1),
    [sym__DIGITS] = ACTIONS(1),
    [sym__SIGN] = ACTIONS(1),
    [anon_sym_STAR] = ACTIONS(1),
    [anon_sym_SLASH] = ACTIONS(1),
    [anon_sym_CARET] = ACTIONS(1),
    [anon_sym_STAR_STAR] = ACTIONS(1),
    [aux_sym_unit_token1] = ACTIONS(1),
    [anon_sym_u00b0] = ACTIONS(1),
    [anon_sym_PERCENT] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
  },
  [1] = {
    [sym_expression] = STATE(49),
    [sym__sub_expression] = STATE(54),
    [sym_variable] = STATE(54),
    [sym__scalar] = STATE(54),
    [sym__number] = STATE(54),
    [sym_integer] = STATE(54),
    [sym_float] = STATE(9),
    [sym_quantity] = STATE(54),
    [sym_call] = STATE(54),
    [anon_sym_DOT] = ACTIONS(3),
    [sym_NAME] = ACTIONS(5),
    [sym__DIGITS] = ACTIONS(7),
    [sym__SIGN] = ACTIONS(9),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 8,
    ACTIONS(3), 1,
      anon_sym_DOT,
    ACTIONS(5), 1,
      sym_NAME,
    ACTIONS(7), 1,
      sym__DIGITS,
    ACTIONS(9), 1,
      sym__SIGN,
    ACTIONS(11), 1,
      anon_sym_RPAREN,
    STATE(9), 1,
      sym_float,
    STATE(46), 1,
      sym_args,
    STATE(37), 7,
      sym__sub_expression,
      sym_variable,
      sym__scalar,
      sym__number,
      sym_integer,
      sym_quantity,
      sym_call,
  [31] = 7,
    ACTIONS(15), 1,
      anon_sym_STAR,
    ACTIONS(17), 1,
      anon_sym_SLASH,
    STATE(7), 1,
      sym_unit,
    STATE(30), 1,
      aux_sym_units_repeat2,
    STATE(5), 2,
      sym_unit_term,
      aux_sym_units_repeat1,
    ACTIONS(13), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
    ACTIONS(19), 3,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
  [58] = 6,
    ACTIONS(3), 1,
      anon_sym_DOT,
    ACTIONS(5), 1,
      sym_NAME,
    ACTIONS(7), 1,
      sym__DIGITS,
    ACTIONS(9), 1,
      sym__SIGN,
    STATE(9), 1,
      sym_float,
    STATE(43), 7,
      sym__sub_expression,
      sym_variable,
      sym__scalar,
      sym__number,
      sym_integer,
      sym_quantity,
      sym_call,
  [83] = 7,
    ACTIONS(15), 1,
      anon_sym_STAR,
    ACTIONS(17), 1,
      anon_sym_SLASH,
    STATE(7), 1,
      sym_unit,
    STATE(32), 1,
      aux_sym_units_repeat2,
    STATE(6), 2,
      sym_unit_term,
      aux_sym_units_repeat1,
    ACTIONS(19), 3,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
    ACTIONS(21), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [110] = 5,
    ACTIONS(25), 1,
      anon_sym_STAR,
    STATE(7), 1,
      sym_unit,
    STATE(6), 2,
      sym_unit_term,
      aux_sym_units_repeat1,
    ACTIONS(28), 3,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
    ACTIONS(23), 4,
      ts_builtin_sym_end,
      anon_sym_SLASH,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [132] = 3,
    ACTIONS(33), 1,
      anon_sym_STAR,
    ACTIONS(35), 2,
      anon_sym_CARET,
      anon_sym_STAR_STAR,
    ACTIONS(31), 7,
      ts_builtin_sym_end,
      anon_sym_SLASH,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [149] = 2,
    ACTIONS(39), 1,
      anon_sym_STAR,
    ACTIONS(37), 9,
      ts_builtin_sym_end,
      anon_sym_SLASH,
      anon_sym_CARET,
      anon_sym_STAR_STAR,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [164] = 5,
    STATE(3), 1,
      sym_unit_term,
    STATE(7), 1,
      sym_unit,
    STATE(40), 1,
      sym_units,
    ACTIONS(19), 3,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
    ACTIONS(41), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [184] = 1,
    ACTIONS(43), 8,
      ts_builtin_sym_end,
      anon_sym_STAR,
      anon_sym_SLASH,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [195] = 4,
    ACTIONS(47), 1,
      aux_sym_float_token1,
    ACTIONS(49), 1,
      sym__DIGITS,
    ACTIONS(51), 1,
      aux_sym_unit_token1,
    ACTIONS(45), 5,
      ts_builtin_sym_end,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [212] = 4,
    ACTIONS(55), 1,
      aux_sym_float_token1,
    ACTIONS(57), 1,
      sym__DIGITS,
    ACTIONS(59), 1,
      aux_sym_unit_token1,
    ACTIONS(53), 5,
      ts_builtin_sym_end,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [229] = 5,
    ACTIONS(55), 1,
      aux_sym_float_token1,
    ACTIONS(59), 1,
      aux_sym_unit_token1,
    ACTIONS(63), 1,
      anon_sym_DOT,
    ACTIONS(53), 2,
      anon_sym_u00b0,
      anon_sym_PERCENT,
    ACTIONS(61), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [248] = 5,
    ACTIONS(65), 1,
      anon_sym_DOT,
    ACTIONS(67), 1,
      aux_sym_float_token1,
    ACTIONS(69), 1,
      aux_sym_unit_token1,
    ACTIONS(71), 2,
      anon_sym_u00b0,
      anon_sym_PERCENT,
    ACTIONS(43), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [267] = 1,
    ACTIONS(23), 8,
      ts_builtin_sym_end,
      anon_sym_STAR,
      anon_sym_SLASH,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [278] = 1,
    ACTIONS(73), 8,
      ts_builtin_sym_end,
      anon_sym_STAR,
      anon_sym_SLASH,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [289] = 1,
    ACTIONS(61), 8,
      ts_builtin_sym_end,
      anon_sym_STAR,
      anon_sym_SLASH,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [300] = 5,
    ACTIONS(77), 1,
      anon_sym_DOT,
    ACTIONS(79), 1,
      anon_sym_LPAREN,
    STATE(26), 1,
      aux_sym_variable_repeat1,
    STATE(53), 1,
      sym__DOT,
    ACTIONS(75), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [318] = 3,
    ACTIONS(47), 1,
      aux_sym_float_token1,
    ACTIONS(51), 1,
      aux_sym_unit_token1,
    ACTIONS(45), 5,
      ts_builtin_sym_end,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [332] = 3,
    ACTIONS(55), 1,
      aux_sym_float_token1,
    ACTIONS(59), 1,
      aux_sym_unit_token1,
    ACTIONS(53), 5,
      ts_builtin_sym_end,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [346] = 3,
    ACTIONS(83), 1,
      aux_sym_float_token1,
    ACTIONS(85), 1,
      aux_sym_unit_token1,
    ACTIONS(81), 5,
      ts_builtin_sym_end,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [360] = 1,
    ACTIONS(45), 6,
      ts_builtin_sym_end,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [369] = 4,
    ACTIONS(89), 1,
      anon_sym_DOT,
    STATE(23), 1,
      aux_sym_variable_repeat1,
    STATE(53), 1,
      sym__DOT,
    ACTIONS(87), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [384] = 1,
    ACTIONS(81), 6,
      ts_builtin_sym_end,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [393] = 1,
    ACTIONS(92), 6,
      ts_builtin_sym_end,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [402] = 4,
    ACTIONS(77), 1,
      anon_sym_DOT,
    STATE(23), 1,
      aux_sym_variable_repeat1,
    STATE(53), 1,
      sym__DOT,
    ACTIONS(94), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [417] = 1,
    ACTIONS(96), 6,
      ts_builtin_sym_end,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [426] = 3,
    STATE(7), 1,
      sym_unit,
    STATE(33), 1,
      sym_unit_term,
    ACTIONS(19), 3,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
  [438] = 3,
    STATE(7), 1,
      sym_unit,
    STATE(15), 1,
      sym_unit_term,
    ACTIONS(19), 3,
      aux_sym_unit_token1,
      anon_sym_u00b0,
      anon_sym_PERCENT,
  [450] = 3,
    ACTIONS(17), 1,
      anon_sym_SLASH,
    STATE(31), 1,
      aux_sym_units_repeat2,
    ACTIONS(98), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [462] = 3,
    ACTIONS(102), 1,
      anon_sym_SLASH,
    STATE(31), 1,
      aux_sym_units_repeat2,
    ACTIONS(100), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [474] = 3,
    ACTIONS(17), 1,
      anon_sym_SLASH,
    STATE(31), 1,
      aux_sym_units_repeat2,
    ACTIONS(105), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [486] = 1,
    ACTIONS(100), 4,
      ts_builtin_sym_end,
      anon_sym_SLASH,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [493] = 1,
    ACTIONS(87), 4,
      ts_builtin_sym_end,
      anon_sym_DOT,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [500] = 3,
    ACTIONS(107), 1,
      anon_sym_RPAREN,
    ACTIONS(109), 1,
      anon_sym_COMMA,
    STATE(41), 1,
      aux_sym_args_repeat1,
  [510] = 3,
    ACTIONS(111), 1,
      sym__DIGITS,
    ACTIONS(113), 1,
      sym__SIGN,
    STATE(16), 1,
      sym_integer,
  [520] = 3,
    ACTIONS(109), 1,
      anon_sym_COMMA,
    ACTIONS(115), 1,
      anon_sym_RPAREN,
    STATE(35), 1,
      aux_sym_args_repeat1,
  [530] = 1,
    ACTIONS(117), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [536] = 1,
    ACTIONS(119), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [542] = 1,
    ACTIONS(121), 3,
      ts_builtin_sym_end,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [548] = 3,
    ACTIONS(123), 1,
      anon_sym_RPAREN,
    ACTIONS(125), 1,
      anon_sym_COMMA,
    STATE(41), 1,
      aux_sym_args_repeat1,
  [558] = 2,
    ACTIONS(128), 1,
      anon_sym_DOT,
    ACTIONS(130), 1,
      sym__DIGITS,
  [565] = 1,
    ACTIONS(123), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [570] = 1,
    ACTIONS(132), 1,
      sym__DIGITS,
  [574] = 1,
    ACTIONS(134), 1,
      sym__DIGITS,
  [578] = 1,
    ACTIONS(136), 1,
      anon_sym_RPAREN,
  [582] = 1,
    ACTIONS(138), 1,
      sym__DIGITS,
  [586] = 1,
    ACTIONS(140), 1,
      sym__DIGITS,
  [590] = 1,
    ACTIONS(142), 1,
      ts_builtin_sym_end,
  [594] = 1,
    ACTIONS(144), 1,
      sym__DIGITS,
  [598] = 1,
    ACTIONS(57), 1,
      sym__DIGITS,
  [602] = 1,
    ACTIONS(146), 1,
      sym__DIGITS,
  [606] = 1,
    ACTIONS(148), 1,
      sym_NAME,
  [610] = 1,
    ACTIONS(150), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 31,
  [SMALL_STATE(4)] = 58,
  [SMALL_STATE(5)] = 83,
  [SMALL_STATE(6)] = 110,
  [SMALL_STATE(7)] = 132,
  [SMALL_STATE(8)] = 149,
  [SMALL_STATE(9)] = 164,
  [SMALL_STATE(10)] = 184,
  [SMALL_STATE(11)] = 195,
  [SMALL_STATE(12)] = 212,
  [SMALL_STATE(13)] = 229,
  [SMALL_STATE(14)] = 248,
  [SMALL_STATE(15)] = 267,
  [SMALL_STATE(16)] = 278,
  [SMALL_STATE(17)] = 289,
  [SMALL_STATE(18)] = 300,
  [SMALL_STATE(19)] = 318,
  [SMALL_STATE(20)] = 332,
  [SMALL_STATE(21)] = 346,
  [SMALL_STATE(22)] = 360,
  [SMALL_STATE(23)] = 369,
  [SMALL_STATE(24)] = 384,
  [SMALL_STATE(25)] = 393,
  [SMALL_STATE(26)] = 402,
  [SMALL_STATE(27)] = 417,
  [SMALL_STATE(28)] = 426,
  [SMALL_STATE(29)] = 438,
  [SMALL_STATE(30)] = 450,
  [SMALL_STATE(31)] = 462,
  [SMALL_STATE(32)] = 474,
  [SMALL_STATE(33)] = 486,
  [SMALL_STATE(34)] = 493,
  [SMALL_STATE(35)] = 500,
  [SMALL_STATE(36)] = 510,
  [SMALL_STATE(37)] = 520,
  [SMALL_STATE(38)] = 530,
  [SMALL_STATE(39)] = 536,
  [SMALL_STATE(40)] = 542,
  [SMALL_STATE(41)] = 548,
  [SMALL_STATE(42)] = 558,
  [SMALL_STATE(43)] = 565,
  [SMALL_STATE(44)] = 570,
  [SMALL_STATE(45)] = 574,
  [SMALL_STATE(46)] = 578,
  [SMALL_STATE(47)] = 582,
  [SMALL_STATE(48)] = 586,
  [SMALL_STATE(49)] = 590,
  [SMALL_STATE(50)] = 594,
  [SMALL_STATE(51)] = 598,
  [SMALL_STATE(52)] = 602,
  [SMALL_STATE(53)] = 606,
  [SMALL_STATE(54)] = 610,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(47),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [13] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_units, 1, 0, 2),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(8),
  [21] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_units, 2, 0, 5),
  [23] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_units_repeat1, 2, 0, 0),
  [25] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_units_repeat1, 2, 0, 0), SHIFT_REPEAT(29),
  [28] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_units_repeat1, 2, 0, 0), SHIFT_REPEAT(8),
  [31] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_unit_term, 1, 0, 3),
  [33] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_unit_term, 1, 0, 3),
  [35] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [37] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_unit, 1, 0, 0),
  [39] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_unit, 1, 0, 0),
  [41] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__number, 1, 0, 0),
  [43] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_integer, 1, 0, 0),
  [45] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_float, 3, 0, 0),
  [47] = {.entry = {.count = 1, .reusable = false}}, SHIFT(45),
  [49] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [51] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_float, 3, 0, 0),
  [53] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_float, 2, 0, 0),
  [55] = {.entry = {.count = 1, .reusable = false}}, SHIFT(44),
  [57] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [59] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_float, 2, 0, 0),
  [61] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_integer, 2, 0, 0),
  [63] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [65] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [67] = {.entry = {.count = 1, .reusable = false}}, SHIFT(48),
  [69] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_float, 1, 0, 0),
  [71] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_float, 1, 0, 0),
  [73] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_unit_term, 3, 0, 9),
  [75] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_variable, 1, 0, 0),
  [77] = {.entry = {.count = 1, .reusable = true}}, SHIFT(53),
  [79] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [81] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_float, 4, 0, 0),
  [83] = {.entry = {.count = 1, .reusable = false}}, SHIFT(52),
  [85] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_float, 4, 0, 0),
  [87] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_variable_repeat1, 2, 0, 0),
  [89] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_variable_repeat1, 2, 0, 0), SHIFT_REPEAT(53),
  [92] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_float, 5, 0, 0),
  [94] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_variable, 2, 0, 0),
  [96] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_float, 6, 0, 0),
  [98] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_units, 2, 0, 6),
  [100] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_units_repeat2, 2, 0, 0),
  [102] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_units_repeat2, 2, 0, 0), SHIFT_REPEAT(28),
  [105] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_units, 3, 0, 8),
  [107] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args, 2, 0, 0),
  [109] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [111] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [113] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [115] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args, 1, 0, 0),
  [117] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_call, 3, 0, 4),
  [119] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_call, 4, 0, 7),
  [121] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quantity, 2, 0, 1),
  [123] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_args_repeat1, 2, 0, 0),
  [125] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_args_repeat1, 2, 0, 0), SHIFT_REPEAT(4),
  [128] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
  [130] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [132] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [134] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [136] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [138] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [140] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [142] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [144] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [146] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [148] = {.entry = {.count = 1, .reusable = true}}, SHIFT(34),
  [150] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_expression, 1, 0, 0),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef TREE_SITTER_HIDE_SYMBOLS
#define TS_PUBLIC
#elif defined(_WIN32)
#define TS_PUBLIC __declspec(dllexport)
#else
#define TS_PUBLIC __attribute__((visibility("default")))
#endif

TS_PUBLIC const TSLanguage *tree_sitter_caqtus(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .field_names = ts_field_names,
    .field_map_slices = ts_field_map_slices,
    .field_map_entries = ts_field_map_entries,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
