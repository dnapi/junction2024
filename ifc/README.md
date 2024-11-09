
Manual on ifcopenshell is here
https://docs.ifcopenshell.org/ifcopenshell-python/hello_world.html



# Standard Shape Entities in IFC Files

In IFC files, specific entities are used to represent standard shape profiles. These predefined geometric profiles simplify the modeling of common cross-sections in building elements such as beams, columns, and pipes.

## 1. **IfcRectangleProfileDef**
- **Purpose**: Defines a rectangular profile.
- **Attributes**:
  - `XDim`: Width of the rectangle.
  - `YDim`: Height of the rectangle.
- **Use Case**: Rectangular beams, columns, or slabs.

## 2. **IfcCircleProfileDef**
- **Purpose**: Represents a circular profile.
- **Attributes**:
  - `Radius`: Radius of the circle.
- **Use Case**: Circular columns, pipes, and cylindrical objects.

## 3. **IfcIShapeProfileDef**
- **Purpose**: Describes an I-shaped (or H-shaped) profile.
- **Attributes**:
  - `OverallWidth`: Width of the flange.
  - `OverallDepth`: Height of the profile.
  - `WebThickness`: Thickness of the web.
  - `FlangeThickness`: Thickness of the flanges.
- **Use Case**: Steel beams, girders, and structural members with I-shaped cross-sections.

## 4. **IfcTShapeProfileDef**
- **Purpose**: Defines a T-shaped profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`: Similar to `IfcIShapeProfileDef`, but tailored for T-shaped sections.
- **Use Case**: Structural beams and supports with T-shaped cross-sections.

## 5. **IfcLShapeProfileDef**
- **Purpose**: Represents an L-shaped (angle) profile.
- **Attributes**:
  - `OverallWidth`: Width of one leg.
  - `OverallDepth`: Width of the other leg.
  - `Thickness`: Thickness of the profile.
- **Use Case**: Angle sections for supports, trusses, and connections.

## 6. **IfcUShapeProfileDef**
- **Purpose**: Defines a U-shaped (channel) profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`.
- **Use Case**: Channels for structural framing, purlins, and beams.

## 7. **IfcCShapeProfileDef**
- **Purpose**: Represents a C-shaped (similar to a channel but with different proportioning) profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`.
- **Use Case**: Beams and sections that need a C-shaped profile.

## 8. **IfcZShapeProfileDef**
- **Purpose**: Describes a Z-shaped profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`.
- **Use Case**: Structural members and trusses with Z-shaped cross-sections.

## 9. **IfcEllipseProfileDef**
- **Purpose**: Defines an elliptical profile.
- **Attributes**:
  - `SemiAxis1`: Length of the first semi-axis.
  - `SemiAxis2`: Length of the second semi-axis.
- **Use Case**: Decorative columns or features with an elliptical cross-section.

## 10. **IfcTrapeziumProfileDef**
- **Purpose**: Represents a trapezoidal profile.
- **Attributes**:
  - `BottomXDim`, `TopXDim`: Length of the bottom and top sides.
  - `YDim`: Vertical height of the trapezoid.
- **Use Case**: Tapered beams or supports.

## 11. **IfcParameterizedProfileDef**
- **Purpose**: Abstract base class for all parametric (standard) profile definitions. All the above entities inherit from this class.
- **Use Case**: Used as the basis for creating other standard profiles based on predefined parameters.

# Usage in IFC Files
- These profiles are commonly used with entities like `IfcExtrudedAreaSolid` to create 3D elements.
- Standard profile types ensure consistency and simplify data exchange in BIM projects by providing ready-made templates for cross-sections.



# Classes Similar to IfcArbitraryClosedProfileDef

Classes similar to `IfcArbitraryClosedProfileDef` in IFC files define profile shapes used for geometry and modeling. These classes describe various profile types, some of which are arbitrary while others are parameterized or predefined.

## 1. **IfcArbitraryClosedProfileDef**
- **Purpose**: Defines an arbitrary closed 2D profile by a closed curve.
- **Attributes**:
  - `OuterCurve`: The curve that defines the closed boundary of the profile.
- **Use Case**: Used for custom cross-sections that do not conform to standard shapes, such as complex window frames or custom structural sections.

## 2. **IfcArbitraryOpenProfileDef**
- **Purpose**: Represents an open curve profile that can be used for defining the cross-section of elements where the profile is not closed (e.g., paths or rails).
- **Attributes**:
  - `Curve`: The defining open curve of the profile.
 - **Use Case**: Used for structural elements like railings or beams with open cross-sections.

## 3. **IfcArbitraryProfileDefWithVoids**
- **Purpose**: Extends `IfcArbitraryClosedProfileDef` by allowing voids within the profile, creating holes in a closed profile.
- **Attributes**:
  - `OuterCurve`: The outer boundary of the profile.
  - `InnerCurves`: A set of inner curves representing voids.
- **Use Case**: Used for profiles that need cut-outs or holes, such as custom beams or frames with openings.

## 4. **IfcCompositeProfileDef**
- **Purpose**: Combines multiple profiles into a single, composite profile definition.
- **Attributes**:
  - `Profiles`: A list of `IfcProfileDef` instances combined to create a complex shape.
  - `Label`: Optional label to name the composite profile.
- **Use Case**: Complex shapes that require a combination of different profile types (e.g., a built-up steel section).

## 5. **IfcDerivedProfileDef**
- **Purpose**: Represents a profile that is derived from another profile by applying transformations like translation, rotation, or scaling.
- **Attributes**:
  - `ParentProfile`: The base profile from which the derived profile is created.
  - `Operator`: The transformation applied to the parent profile.
  - `Label`: Optional name for the derived profile.
- **Use Case**: Custom or modified profiles that need a simple transformation of an existing shape.

## 6. **IfcParameterizedProfileDef**
- **Purpose**: The abstract base class for all parameterized profiles. These profiles have specific parameters that define their shape (e.g., width, height).
- **Subclasses**: Includes `IfcRectangleProfileDef`, `IfcCircleProfileDef`, `IfcIShapeProfileDef`, and more.
- **Use Case**: Defines standard shapes using predefined parameters for consistent modeling.

## 7. **IfcCenterLineProfileDef**
- **Purpose**: Used for defining profiles that have a specific center line.
- **Attributes**:
  - `Curve`: The defining center curve for the profile.
- **Use Case**: Typically used in defining roads, rail tracks, or structural elements where the centerline needs to be explicitly defined.

## 8. **IfcAsymmetricIShapeProfileDef**
- **Purpose**: A specialized version of the `IfcIShapeProfileDef` for asymmetric I-shaped profiles.
- **Attributes**:
  - Same as `IfcIShapeProfileDef` but includes parameters for asymmetry.
- **Use Case**: I-beams or girders that have unequal flange sizes.

## 9. **IfcTrapeziumProfileDef**
- **Purpose**: Represents a trapezoidal profile used for various elements with a trapezoidal cross-section.
- **Attributes**:
  - `BottomXDim`, `TopXDim`, `YDim`, etc.
- **Use Case**: Tapered beams or supports.

## 10. **IfcRoundedRectangleProfileDef**
- **Purpose**: Represents a rectangle with rounded corners.
- **Attributes**:
  - `XDim`, `YDim`: Width and height of the rectangle.
  - `RoundingRadius`: Radius of the rounded corners.
- **Use Case**: Structural or architectural components requiring a rounded profile.

## 11. **IfcEllipseProfileDef**
- **Purpose**: Represents an elliptical profile.
- **Attributes**:
  - `SemiAxis1`, `SemiAxis2`: Lengths of the semi-major and semi-minor axes.
- **Use Case**: Columns or decorative features with an elliptical shape.

# Summary
These profile classes in IFC files provide flexibility in defining both standard and custom cross-sections for various elements in a building model. From simple, parameterized profiles to more complex composite or derived ones, these entities support detailed and varied structural modeling.
