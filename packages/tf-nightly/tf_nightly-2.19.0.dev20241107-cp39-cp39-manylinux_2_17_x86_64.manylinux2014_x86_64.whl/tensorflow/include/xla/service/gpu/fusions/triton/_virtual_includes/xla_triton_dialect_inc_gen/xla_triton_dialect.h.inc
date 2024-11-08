/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Dialect Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: xla_triton_dialect.td                                                *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace triton {
namespace xla {

class XlaTritonDialect : public ::mlir::Dialect {
  explicit XlaTritonDialect(::mlir::MLIRContext *context);

  void initialize();
  friend class ::mlir::MLIRContext;
public:
  ~XlaTritonDialect() override;
  static constexpr ::llvm::StringLiteral getDialectNamespace() {
    return ::llvm::StringLiteral("triton_xla");
  }
};
} // namespace xla
} // namespace triton
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::triton::xla::XlaTritonDialect)
