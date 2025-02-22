# File Formats


| Feature                   | JSON  | Fix Length | Delimited | Custom Columnar |
|---------------------------|------|------------|-----------|-----------------|
| **Schema Flexibility**    | ✅ High  | ❌ Rigid      | ⚠️ Moderate   | ⚠️ Moderate         |
| **Readability**           | ✅ High  | ✅ High       | ⚠️ Moderate   | ⚠️ Moderate         |
| **Storage Efficiency**    | ❌ Redundant keys | ❌ Padding spaces | ✅ Compact | ✅ Best |
| **Parsing Efficiency**    | ⚠️ Text overhead | ✅ Fast offset-based | ❌ Text overhead | ✅ Binary representation |
| **Metadata Info**         | ✅ Self documenting | ❌ None       | ❌ None       | ❌ None             |
| **Nested Data Support**   | ✅ Full  | ❌ None       | ⚠️ Partial    | ⚠️ Partial          |
| **Query Speed (Row-based)** | ✅ Fast | ✅ Fast | ✅ Fast | ❌ Slow |
| **Query Speed (Column-based)** | ❌ Slow | ❌ Slow | ❌ Slow | ✅ Very Fast |
| **Compression**           | ❌ Inefficient | ❌ Inefficient | ⚠️ Moderate | ✅ High |
| **Type Enforcing**        | ❌ None  | ❌ None       | ❌ None       | ❌ None             |
| **Schema Evolution**      | ✅ Easy  | ❌ Difficult  | ❌ Difficult  | ✅ Easy        |
| **Adding New Field**  | ✅ Anywhere | ❌ Only at end | ❌ Only at end | ✅ Easy |
| **Row Delete**     | ✅ Easy  | ✅ Easy | ✅ Easy | ❌ Challenging |
| **Column Drop**     | ❌ Challenging  | ❌ Challenging | ❌ Challenging | ✅ Easy |