GEN_TYPING_TARGETS += src/qtk/array_types/array/__init__.pyi
GEN_TYPING_TARGETS += src/qtk/array_types/array/_bool.py
GEN_TYPING_TARGETS += src/qtk/array_types/array/_float.py
GEN_TYPING_TARGETS += src/qtk/array_types/array/_integer.py
GEN_TYPING_TARGETS += src/qtk/array_types/jax/__init__.pyi
GEN_TYPING_TARGETS += src/qtk/array_types/jax/_bool.py
GEN_TYPING_TARGETS += src/qtk/array_types/jax/_export.py
GEN_TYPING_TARGETS += src/qtk/array_types/jax/_float.py
GEN_TYPING_TARGETS += src/qtk/array_types/jax/_integer.py
GEN_TYPING_TARGETS += src/qtk/array_types/numpy/__init__.pyi
GEN_TYPING_TARGETS += src/qtk/array_types/numpy/_bool.py
GEN_TYPING_TARGETS += src/qtk/array_types/numpy/_export.py
GEN_TYPING_TARGETS += src/qtk/array_types/numpy/_float.py
GEN_TYPING_TARGETS += src/qtk/array_types/numpy/_integer.py
GEN_TYPING_TARGETS += src/qtk/array_types/torch/__init__.pyi
GEN_TYPING_TARGETS += src/qtk/array_types/torch/_bool.py
GEN_TYPING_TARGETS += src/qtk/array_types/torch/_export.py
GEN_TYPING_TARGETS += src/qtk/array_types/torch/_float.py
GEN_TYPING_TARGETS += src/qtk/array_types/torch/_integer.py

.PHONY: $(GEN_TYPING_TARGETS)
gen-array-types: $(GEN_TYPING_TARGETS)

# ----------------------------- Auxiliary Targets ---------------------------- #

$(GEN_TYPING_TARGETS): src/qtk/%: templates/%.jinja scripts/gen-array-types.py
	@ python scripts/gen-array-types.py --output "$@" "$<"
	@ ruff check "$@"
