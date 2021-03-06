
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'U\xde\xb4\x15\x93\x8b\x88\xd0\xc3l\x01!\xd4\xf8q\xa7'
    
_lr_action_items = {'LPAR':([0,1,9,13,14,15,16,17,19,],[1,1,1,1,1,1,1,1,1,]),'CONSTANT':([0,1,9,13,14,15,16,17,19,],[3,3,3,3,3,3,3,3,3,]),'DIVIDE':([3,4,5,7,8,10,11,12,18,20,21,22,23,24,25,26,27,28,29,],[-15,-13,-16,13,-14,-18,-13,13,-12,-4,-17,-5,-6,-10,-9,13,-11,13,13,]),'NUMBER':([0,1,9,13,14,15,16,17,19,],[5,5,5,5,5,5,5,5,5,]),'TIMES':([3,4,5,7,8,10,11,12,18,20,21,22,23,24,25,26,27,28,29,],[-15,-13,-16,14,-14,-18,-13,14,-12,-4,-17,-5,-6,-10,-9,14,-11,14,14,]),'PLUS':([3,4,5,7,8,10,11,12,18,20,21,22,23,24,25,26,27,28,29,],[-15,-13,-16,15,-14,-18,-13,15,-12,-4,-17,-5,-6,-10,-9,-7,-11,15,-8,]),'EXP':([3,4,5,7,8,10,11,12,18,20,21,22,23,24,25,26,27,28,29,],[-15,-13,-16,16,-14,-18,-13,16,-12,-4,-17,-5,-6,16,16,16,-11,16,16,]),'IN':([3,4,5,7,8,10,18,20,21,22,23,24,25,26,27,29,],[-15,-13,-16,17,-14,-18,-12,-4,-17,-5,-6,-10,-9,-7,-11,-8,]),'RPAR':([3,4,5,8,10,11,12,18,20,21,22,23,24,25,26,27,29,],[-15,-13,-16,-14,-18,22,23,-12,-4,-17,-5,-6,-10,-9,-7,-11,-8,]),'MINUS':([0,1,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,],[9,9,-15,-13,-16,19,-14,9,-18,-13,19,9,9,9,9,9,-12,9,-4,-17,-5,-6,-10,-9,-7,-11,19,-8,]),'UNIT':([0,1,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,],[10,10,-15,-13,-16,10,-14,10,10,-13,10,10,10,10,10,10,-12,10,-4,-17,-5,-6,-10,-9,-7,-11,10,-8,]),'$end':([2,3,4,5,6,7,8,10,18,20,21,22,23,24,25,26,27,28,29,],[-1,-15,-13,-16,0,-2,-14,-18,-12,-4,-17,-5,-6,-10,-9,-7,-11,-3,-8,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'units':([0,1,7,9,10,12,13,14,15,16,17,19,20,24,25,26,27,28,29,],[8,8,18,8,21,18,8,8,8,8,8,8,18,18,18,18,18,18,18,]),'expr':([0,1,9,13,14,15,16,17,19,],[4,11,4,4,4,4,4,4,4,]),'conversion':([0,],[2,]),'unit-expr':([0,1,9,13,14,15,16,17,19,],[7,12,20,24,25,26,27,28,29,]),'eval-expr':([0,],[6,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> eval-expr","S'",1,None,None,None),
  ('eval-expr -> conversion','eval-expr',1,'p_eval_expr','/Users/stephen/Working/conversion/parser.py',27),
  ('eval-expr -> unit-expr','eval-expr',1,'p_eval_expr','/Users/stephen/Working/conversion/parser.py',28),
  ('conversion -> unit-expr IN unit-expr','conversion',3,'p_conversion','/Users/stephen/Working/conversion/parser.py',33),
  ('unit-expr -> MINUS unit-expr','unit-expr',2,'p_expr_unary','/Users/stephen/Working/conversion/parser.py',38),
  ('expr -> LPAR expr RPAR','expr',3,'p_expr_paren','/Users/stephen/Working/conversion/parser.py',42),
  ('unit-expr -> LPAR unit-expr RPAR','unit-expr',3,'p_unit_expr_paren','/Users/stephen/Working/conversion/parser.py',47),
  ('unit-expr -> unit-expr PLUS unit-expr','unit-expr',3,'p_expr_binop','/Users/stephen/Working/conversion/parser.py',52),
  ('unit-expr -> unit-expr MINUS unit-expr','unit-expr',3,'p_expr_binop','/Users/stephen/Working/conversion/parser.py',53),
  ('unit-expr -> unit-expr TIMES unit-expr','unit-expr',3,'p_expr_binop','/Users/stephen/Working/conversion/parser.py',54),
  ('unit-expr -> unit-expr DIVIDE unit-expr','unit-expr',3,'p_expr_binop','/Users/stephen/Working/conversion/parser.py',55),
  ('unit-expr -> unit-expr EXP unit-expr','unit-expr',3,'p_expr_binop','/Users/stephen/Working/conversion/parser.py',56),
  ('unit-expr -> unit-expr units','unit-expr',2,'p_unit_expr','/Users/stephen/Working/conversion/parser.py',73),
  ('unit-expr -> expr','unit-expr',1,'p_unit_expr_one','/Users/stephen/Working/conversion/parser.py',78),
  ('unit-expr -> units','unit-expr',1,'p_unit_expr_one','/Users/stephen/Working/conversion/parser.py',79),
  ('expr -> CONSTANT','expr',1,'p_expr_constant','/Users/stephen/Working/conversion/parser.py',84),
  ('expr -> NUMBER','expr',1,'p_expr_literal','/Users/stephen/Working/conversion/parser.py',89),
  ('units -> UNIT units','units',2,'p_units_units','/Users/stephen/Working/conversion/parser.py',95),
  ('units -> UNIT','units',1,'p_units_unit','/Users/stephen/Working/conversion/parser.py',99),
]
